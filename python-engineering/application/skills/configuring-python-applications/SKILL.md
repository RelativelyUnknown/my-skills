---
name: configuring-python-applications
description: "Use when adding settings, environment variables, a config file or secrets, or when a missing variable fails at the wrong time. Load config once at the entry point, parse explicitly, report every error at startup, keep secrets out of logs, .env for development only."
license: MIT
metadata:
  adapted-from: "wshobson/agents python-configuration (MIT, Seth Hobson); see SOURCE.md"
---

# Configuring Python applications

Defaults: read the `## Python defaults` section of AGENTS.md; infer what is missing from the repo; ask only what is still unknown, once; save the answers there. Match the project: a dataclass with `os.environ` and `tomllib` (3.11+) is enough for a handful of settings; use `pydantic-settings` when the project already uses pydantic. Checked on Python 3.13 with pydantic-settings 2.15.0 on 7 November 2026.

## Rules

- Load once, at the entry point: build a frozen config object from the environment and any file, validate it, and pass it in. No `settings = Settings()` at import: a missing variable then breaks tests, documentation builds and every tool that imports the module, and a global hides what each function needs. A library takes its configuration as arguments and reads no environment.
- Precedence is written in one place: command-line argument, then environment variable, then config file, then a literal default in the config class.
- Parse explicitly. `os.environ["PORT"]` raises `KeyError('PORT')` when it is missing and `int("80a")` raises `ValueError`. `bool("false")` is `True`, so parse booleans against a set (`"1"`, `"true"`, `"yes"`, `"on"`). pydantic-settings turns `"false"` into `False` and a bad `int` into an error naming the field.
- Fail at startup and report every problem at once: collect the errors and raise one exception that lists all missing or invalid names. pydantic-settings does this by default (`database_url` and `api_key` both reported missing in one `ValidationError`).
- One prefix per application (`APP_DATABASE_URL`), one name per setting, nested groups with a delimiter (`env_nested_delimiter="__"` makes `APP_DB__POOL_SIZE` a field of `db`). Describe each variable (type, default, meaning) next to the config class, and commit a `.env.example` with no real values. `.env` is for development, in `.gitignore`.
- Secrets come from the environment or a mounted file (container secrets are files; the `*_FILE` convention). Keep them out of `repr` and logs: `SecretStr` in pydantic, `field(repr=False)` in a dataclass. Never default a secret to a plausible value. pydantic-settings reads a secrets directory with file names built from the prefix in lower case (`app_api_key`).
- pydantic-settings precedence, highest first: values passed to the constructor, environment, dotenv file, secrets directory, defaults.
- Environments differ in values, not in code paths: no `if ENV == "production":` in business logic. A feature flag is a typed boolean that defaults to off, with an owner and a removal date.
- Defaults are literals in the config class, not module constants. Read the environment in the loader only; scattered `os.getenv` calls cannot be validated together.
- Tests build the config object directly (`make_config(**overrides)`) and test the loader with `monkeypatch.setenv` / `delenv`. Construct pydantic settings with `_env_file=None` in tests so a developer's `.env` does not leak in.

Runnable examples: [references/patterns.md](references/patterns.md).
