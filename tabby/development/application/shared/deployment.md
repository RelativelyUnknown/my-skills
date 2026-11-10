# Deployment and operations

## Servers and workers

- Container platform (Kubernetes, ECS, Cloud Run): One server process per container (`fastapi run`, which needs `fastapi[standard]`, or `uvicorn <pkg>.main:app --host 0.0.0.0 --port 8000`); scale by replicas
- A single VM: `uvicorn ... --workers N`, or gunicorn with the `uvicorn-worker` package's worker class; N from load tests, starting near the CPU count
- Higher throughput needed and measured: granian (`granian --interface asgi <pkg>.main:app`), after a load test against the real app
- Django without async views: gunicorn (WSGI)

- Behind a reverse proxy or load balancer: enable proxy headers (`--proxy-headers --forwarded-allow-ips=<proxy IPs>`) so client IPs and schemes are correct; never trust forwarded headers from everyone.
- The `uvicorn.workers.UvicornWorker` class inside uvicorn is deprecated; use the separate `uvicorn-worker` package.
- Size connection pools so that pool size times the number of processes stays under the database's connection limit.

## Container image

```dockerfile
FROM python:3.12-slim AS build
COPY --from=ghcr.io/astral-sh/uv:<version> /uv /bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY src ./src
RUN uv sync --locked --no-dev

FROM python:3.12-slim
RUN useradd --create-home app
COPY --from=build --chown=app /app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["fastapi", "run", "/app/src/<pkg>/main.py", "--port", "8000"]
```

- Dependencies install in a layer before the source, so code changes do not reinstall them.
- Pin the base image and the uv image to versions (or digests); run as a non-root user; no secrets in build args or layers.
- Match the image's Python minor version to `requires-python` and CI.

## Health and shutdown

- Liveness endpoint: returns 200 if the process can serve; no dependency checks (a database outage must not restart every pod).
- Readiness endpoint: checks what the service needs to take traffic (database ping, required caches).
- Graceful shutdown: the lifespan closes clients and pools; the platform's termination grace period exceeds the longest request.

## Logging

- Structured (JSON) logs to stdout with level, message, logger, request ID, and route; configure once at startup (stdlib `logging` with a JSON formatter, or structlog).
- Generate or accept a request ID per request (middleware) and include it in every log line and error response.
- Never log tokens, passwords, full request bodies or personal data; log IDs.
- Library code still uses `logging.getLogger(__name__)` without configuring handlers ([logging.md](../../code/logging.md)).

## Metrics and tracing

- OpenTelemetry when the organization runs a collector: `opentelemetry-instrumentation-fastapi` (or `-django`), plus instrumentations for the database driver and HTTP client, configured through `OTEL_*` environment variables.
- At minimum, request rate, error rate and latency per route, and database pool usage.

## Configuration

- Twelve-factor: all configuration from environment variables, validated at startup by the settings model. A missing required setting fails the deploy, not the first request.
- Secrets come from the platform's secret store into environment variables or mounted files; never from the image or the repository.
- Migrations run as a separate step before the new version takes traffic (`persistence.md`).
