# Observability patterns

The first block uses only the standard library. The others need `prometheus-client` and `opentelemetry-api` plus `opentelemetry-sdk`; they were run in a scratch environment on 7 November 2026.

## Contents

- JSON logs with a request id
- Timing a block
- Request metrics with bounded labels
- Spans that share a trace

## JSON logs with a request id

```python
import asyncio
import contextvars
import json
import logging
import logging.config
import sys

request_id = contextvars.ContextVar("request_id", default="-")


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id.get()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {"level": record.levelname, "logger": record.name, "msg": record.getMessage(),
                "request_id": record.request_id}
        if record.exc_info:
            data["exc"] = self.formatException(record.exc_info).splitlines()[-1]
        return json.dumps(data)


logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"ctx": {"()": ContextFilter}},
    "formatters": {"json": {"()": JsonFormatter}},
    "handlers": {"out": {"class": "logging.StreamHandler", "stream": sys.stdout,
                         "formatter": "json", "filters": ["ctx"]}},
    "root": {"level": "INFO", "handlers": ["out"]},
})
log = logging.getLogger("app")


async def handle(rid: str) -> None:
    request_id.set(rid)
    await asyncio.sleep(0.01)
    await asyncio.to_thread(lambda: log.info("in thread"))  # keeps this request's id


async def main() -> None:
    await asyncio.gather(handle("r1"), handle("r2"))


asyncio.run(main())
```

## Timing a block

```python
import time
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def timed(sink: dict[str, float], name: str) -> Iterator[None]:
    start = time.perf_counter()  # monotonic: unaffected by clock changes
    try:
        yield
    finally:
        sink[name] = time.perf_counter() - start


timings: dict[str, float] = {}
with timed(timings, "work"):
    sum(range(1000))
assert timings["work"] >= 0
```

## Request metrics with bounded labels

```python
from prometheus_client import CollectorRegistry, Counter, Histogram, generate_latest

registry = CollectorRegistry()
requests = Counter("http_requests", "Requests", ["method", "route", "status"], registry=registry)
latency = Histogram("http_request_duration_seconds", "Latency", ["route"], registry=registry,
                    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5))

route = "/orders/{id}"  # the template from the router, never request.url.path
requests.labels("GET", route, "200").inc()
latency.labels(route).observe(0.08)
assert b"http_requests_total" in generate_latest(registry)
```

## Spans that share a trace

```python
import asyncio

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.trace import Status, StatusCode


class Keep(SpanExporter):
    spans: list = []

    def export(self, spans):
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS


provider = TracerProvider(resource=Resource.create({"service.name": "shop"}))
provider.add_span_processor(SimpleSpanProcessor(Keep()))
trace.set_tracer_provider(provider)  # once, at the entry point
tracer = trace.get_tracer("shop.orders")  # libraries only call get_tracer


async def query() -> None:
    with tracer.start_as_current_span("db.query"):
        await asyncio.sleep(0.01)


async def handler() -> None:
    with tracer.start_as_current_span("POST /orders") as span:
        await asyncio.gather(query(), query())
        error = ValueError("bad coupon")
        span.record_exception(error)
        span.set_status(Status(StatusCode.ERROR, "bad coupon"))


asyncio.run(handler())
root = next(s for s in Keep.spans if s.name == "POST /orders")
assert all(s.parent.span_id == root.context.span_id for s in Keep.spans if s.name == "db.query")
```
