# HTTP services

A web service is a public API with a database behind it: validate everything coming in, return only what you mean to, and never block the event loop. Python code rules: [snags.md](../../../all/code/snags.md); test rules: [testing.md](../../../all/testing/testing.md).

## Start

Read `pyproject.toml` for the framework, ORM, server and auth libraries in use.

- Use the framework, ORM, server and auth library the project has. Never add a second framework or ORM; never migrate frameworks unless asked.
- Running migrations against a shared database, changing auth or CORS settings, and deleting endpoints need approval.

## Every change

1. **Validate at the boundary.** Request bodies, query parameters, path parameters and headers go through typed models (Pydantic v2, or the framework's own). No `dict` bodies, no manual `request.json()` parsing.
2. **Explicit responses.** Every endpoint declares its response model. Never return ORM objects, internal dicts or exception text; extra fields leak data.
3. **Authorization per object.** Check that the caller may act on *this* record in the handler or service, not only that they are logged in. Broken object-level authorization is the top API vulnerability (OWASP API1).
4. **Settings from the environment.** `pydantic-settings` or Django settings read from environment variables; no secrets or production URLs in code, defaults or tests.
5. **Async means non-blocking.** Inside `async def`, only await async drivers and clients. Blocking calls (sync DB drivers, `requests`, file reads of unknown size, CPU-heavy work) go in a plain `def` endpoint (FastAPI runs it in a thread pool) or `run_in_threadpool`/`asyncio.to_thread`.
6. **One client, one pool.** Database engines, HTTP clients and Redis connections are created once at startup (lifespan) and shared; never per request.
7. **Errors are stable.** Map domain errors to HTTP status codes in one place (exception handlers) with a stable error shape; log the details server-side with a request ID.
8. **Tests** for every new endpoint: the success path, a validation failure, an unauthenticated call and a call on another user's object.

## Framework notes

- FastAPI (or Litestar, Starlette): [fastapi.md](fastapi.md)
- Django (with Django Ninja or DRF): [django.md](django.md)
- SQLAlchemy, SQLModel or Alembic: [persistence.md](../../shared/persistence.md)
- Any auth, upload, CORS, rate-limit or outbound-URL change: [security.md](../shared/security.md)
- Dockerfiles, servers, workers, health checks, logging, tracing: [deployment.md](../../shared/deployment.md)

New project with no framework chosen: FastAPI for a typed JSON API; Django when the service needs an admin, auth, templates and an ORM out of the box. Flask only to match an existing codebase. State the choice in the report.

## Background work

- Small, best-effort, same process (send an email after responding): the framework's background tasks.
- Must survive a restart, retry or run on a schedule: a real queue with a worker (Celery, Dramatiq, arq, Taskiq, or a `django.tasks` backend). Django 6's `django.tasks` defines and enqueues tasks but ships no production worker.
- Tasks are idempotent and take IDs, not ORM objects.

## Testing

- FastAPI: `with TestClient(app) as client:` runs the lifespan; for async tests use `httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")` and start the lifespan yourself (for example `asgi-lifespan`), since the transport does not.
- Replace dependencies with `app.dependency_overrides[get_db] = ...`, not `mock.patch`.
- Queries that matter run against the real database engine (a Testcontainers Postgres, or the project's test database), not mocks and not SQLite standing in for Postgres. Roll back or truncate between tests.
- External HTTP calls are mocked at the transport (`respx` for httpx, `responses` for requests).

## Report

Report as in [shipping.md](../../../all/workflow/shipping.md). List endpoints added or changed with their auth requirement, models and migrations created, settings added (names only) and tests added. Name anything that needs approval or a person: secrets, DNS, migrations on shared databases.
