# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-configuration/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (215 lines) and details (162 lines) are condensed to about 10 rules and one examples file.
- Rewritten against the upstream's central pattern, a module-level `settings = Settings()` singleton created at import and `pydantic-settings` for everything. That conflicts with this repository's rules (nothing runs at import, no module-level state, match the project's idiom before adding a package). The rewrite loads once at the entry point, shows a standard-library loader first, and keeps pydantic-settings as the option when the project already uses pydantic.
- Run on Python 3.13 with pydantic 2.14.3 and pydantic-settings 2.15.0 (installed in a scratch environment, not a dependency of this repository): all missing and invalid fields are reported in one `ValidationError`; `"false"` parses to `False`; `SecretStr` stays out of `repr`; constructor values beat the environment; a secrets directory reads files named with the lower-case prefix (`app_api_key`); the order of sources is constructor, environment, dotenv file, secrets directory, default. Plain Python: `bool("false")` is `True`; a missing `os.environ[...]` raises `KeyError`.
- From the pydantic-settings documentation, not run: `env_nested_delimiter` for nested groups.
- Dropped: the type-coercion primer, environment-specific subclass tree, nested group walkthrough and the generic validation checklist.
