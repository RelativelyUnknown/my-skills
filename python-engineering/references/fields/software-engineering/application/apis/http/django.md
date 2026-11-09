# Django

Django 6.0 (December 2025) added `django.tasks`, a built-in Content Security Policy and template partials; Django 6.x supports Python 3.12 and up. Check the installed version before using a 6.x feature.

## Structure

- One app per bounded area (`orders`, `billing`), each with its own models, admin, services and tests. Avoid a `core` or `common` app that everything imports.
- Business logic in service functions or model methods, not in views, serializers or signals. Views parse input, call a service, return a response.
- Settings split by environment through environment variables (`django-environ` or plain `os.environ`), with `DEBUG = False` and an explicit `ALLOWED_HOSTS` in production. `python manage.py check --deploy` passes.

## APIs

- Typed JSON APIs: Django Ninja (Pydantic schemas, FastAPI-like) or Django REST Framework (serializers, viewsets); use whichever the project has.
- Every endpoint declares its input schema and output schema; querysets are filtered by the requesting user before lookup (`Order.objects.filter(owner=request.user).get(pk=pk)`), never fetched first and checked later.

## ORM

- Avoid N+1 queries: `select_related` for foreign keys, `prefetch_related` for reverse and many-to-many relations. Check with `django-debug-toolbar` locally or `assertNumQueries` in tests.
- Writes that must succeed together use `transaction.atomic()`. Side effects after commit (emails, tasks) use `transaction.on_commit`.
- Bulk work uses `bulk_create`, `bulk_update`, `update()` and `iterator()`, not per-row `save()` in a loop.
- Use `F()` expressions for concurrent counters, and `select_for_update()` where rows must be locked.

## Migrations

- Every model change ships its migration (`makemigrations`), reviewed by reading it. Never edit a migration that has run in a shared environment; add a new one.
- Large tables: add nullable columns first, backfill in batches, then add constraints; avoid long locks. Data migrations use `RunPython` with the historical model (`apps.get_model`).
- `makemigrations --check` in CI catches model changes without migrations.

## Async

- Async views and the async ORM interface (`aget`, `acreate`, `async for`) suit I/O-bound fan-out; sync views stay fine for ordinary CRUD. Do not call sync ORM methods from async code; wrap with `sync_to_async` when unavoidable.
- Run under an ASGI server only when the project uses async views or websockets; otherwise WSGI (gunicorn) is simpler.

## Tasks

- `django.tasks` defines tasks with `@task` and enqueues them with `.enqueue()`; a configured backend and a separate worker process do the work (Django itself ships only development backends).
- Pass primary keys, not model instances; make tasks idempotent; enqueue inside `transaction.on_commit`.

## Security settings worth checking

`SECURE_PROXY_SSL_HEADER` behind a proxy, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, CSP configured for the templates in use, `CSRF_TRUSTED_ORIGINS` explicit, password hashers led by Argon2 (`django[argon2]`).
