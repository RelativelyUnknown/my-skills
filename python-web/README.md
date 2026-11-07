# python-web

Part of the [skills monorepo](../README.md).

One agent skill, `building-python-web-services`, for Python web APIs and services: FastAPI first (the stack in [Mallard](https://github.com/RelativelyUnknown/Mallard)'s server), Django, Litestar and Flask where a project already uses them. It builds on the [python-engineering](../python-engineering/) skills and points to them by name (`writing-python-code`, `testing-python-packages`, `designing-package-apis`); install those too.

## Skill

| Skill | Loads when you... | Body (est. tokens) |
| --- | --- | --- |
| `building-python-web-services` | add endpoints, wire a database or auth, or deploy a Python web service | 1.6k |

The body holds eight rules that apply to every change (boundary validation, explicit response models, per-object authorization, settings from the environment, no blocking calls in `async def`, shared clients, stable errors, four tests per endpoint). Detail lives in five references that load only when the task touches them:

| Reference | Covers |
| --- | --- |
| `fastapi.md` | Layout, `Annotated` dependencies, `pydantic-settings`, lifespan, response models, error mapping, Litestar notes |
| `django.md` | App structure, Ninja/DRF, ORM pitfalls (N+1, transactions), migrations, async, `django.tasks` |
| `persistence.md` | SQLAlchemy 2.x models and async sessions, query rules, SQLModel, Alembic |
| `security.md` | OWASP API Security Top 10 (2023) checks, Argon2 via pwdlib, JWT validation, CORS, uploads, SSRF |
| `deployment.md` | Servers and workers, a uv-based Dockerfile, health checks, structured logs, OpenTelemetry |

Faster drop-ins for web code (orjson, msgspec, uvloop, granian) are in `writing-python-code`'s `references/faster-libraries.md`, behind its profile-first rule.

## Evals

`skills/building-python-web-services/evals/` holds a case for an owned-resource endpoint (object-level authorization, response model, tests for another user's object); trigger checks are in `evals/building-python-web-services.triggers.json`.

## Install

```bash
mkdir -p .claude/skills
cp -r /path/to/skills/python-web/skills/* .claude/skills/
cp -r /path/to/skills/python-engineering/skills/{writing-python-code,testing-python-packages} .claude/skills/
```

The skill runs the shared `scripts/detect_project.py` from python-engineering (a copy ships in the skill folder) and accepts the same `python=` and `runner=` arguments.

## Develop

This skillset has no tooling of its own. Check it with the python-engineering checker:

```bash
cd ../python-engineering && uv run python scripts/check_skills.py ../python-web/skills
```

Add `--sync` after changing the canonical `detect_project.py`.

## License

MIT.
