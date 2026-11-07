---
name: adding-observability
description: "Logs, metrics and traces for Python services: one logging config at the entry point, request ids through contextvars, log levels, bounded metric labels, rate-error-duration metrics, OpenTelemetry API versus SDK, error spans. Use when adding logging, metrics, tracing or health signals, or when production failures cannot be traced."
compatibility: "Needs the python-project-facts skill installed in the same folder."
argument-hint: "[python=3.12]"
license: MIT
metadata:
  adapted-from: "wshobson/agents python-observability (MIT, Seth Hobson); see SOURCE.md"
---

# Adding observability

Run `python3 <this skill's folder>/../python-project-facts/scripts/detect_project.py` once. If the facts skill is not installed, tell the user once that project facts are assumed and use defaults. Use the stack the project already has (stdlib `logging`, structlog, Prometheus, an OpenTelemetry collector); add a library only when asked. Checked on Python 3.13 with prometheus-client 0.26.0 and OpenTelemetry 1.45.2 on 7 November 2026.

## Logs

- Configure logging once, at the application entry point (`logging.config.dictConfig`), as JSON lines on stdout. Never at import and never in library code (the library bundle covers library logging, if installed).
- Put the request or job id in a `contextvars.ContextVar` set at the edge, and add it to every record with a `logging.Filter`. It follows `await`, `gather` tasks and `asyncio.to_thread`, so concurrent requests keep their own ids.
- `extra={...}` keys must not collide with record attributes: `extra={"message": ...}` raises `KeyError: "Attempt to overwrite 'message' in LogRecord"`. Prefix them (`order_id`, `job_attempt`).
- Lazy arguments (`log.info("loaded %s rows", n)`), `log.exception(...)` inside `except`, and one line per event. Levels: DEBUG internals; INFO a business event or state change; WARNING something abnormal that was handled; ERROR an operation failed and someone should look (a client's 4xx is not an error).
- Log ids, never secrets, tokens, bodies or personal data.

## Metrics

- Measure at the boundary (middleware, client wrapper, worker loop), not inside every function: requests per second, errors, duration (rate, errors, duration), plus saturation (queue depth, pool in use, oldest job age).
- Label values are bounded: the route template (`/orders/{id}`), not the raw path; a status class or code; never a user id, URL or error message. Every label combination is a new time series (3 routes x 5 statuses x 2 methods is 30). Per-user questions belong in logs.
- Prometheus: base units (seconds, bytes); a counter's name gets `_total`; histogram buckets surround the latency objective; time with `time.perf_counter()`. Several worker processes need the client's multiprocess mode (`PROMETHEUS_MULTIPROC_DIR`; documentation, not run).
- Health: liveness says the process is up, readiness says its dependencies work. Keep them separate (`building-python-web-services`, deployment notes).

## Traces

- Code and libraries import only `opentelemetry-api`. Spans are non-recording no-ops until the application installs `opentelemetry-sdk` and an exporter, so instrumenting a library costs nothing.
- Configure the SDK at the entry point from the environment: `OTEL_SERVICE_NAME`, `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_TRACES_SAMPLER`. `opentelemetry-instrument python app.py` adds framework instrumentation without code changes (documentation, not run).
- Spans started in tasks created by `gather` or a `TaskGroup` become children of the current span. Across a queue or an HTTP call, carry the context in headers (`propagate.inject` / `extract`, the `traceparent` header).
- On failure: `span.record_exception(exc)` and `span.set_status(Status(StatusCode.ERROR, ...))`, then re-raise. Span attributes are bounded and carry no secrets.
- Add the trace id to log lines so a log and its trace can be joined.

Jobs log their id, key and attempt (`running-background-jobs`). Runnable examples: [references/patterns.md](references/patterns.md).
