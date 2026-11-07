# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-type-safety/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- Rewritten as short rules; the upstream body (200 lines) and `references/details.md` (237 lines) are condensed to about 20 rules and one examples file.
- Dropped because they conflict with this repository's rules (no abstraction with one implementation, no `Any`): the generic `Result` class and the generic repository. Dropped as restating the language docs: the primer on annotations and unions.
- Added after running each one with `mypy --strict` 2.4.1 on Python 3.13: list invariance and `Sequence`; `TypeIs` requires the narrowed type to be a subtype of the parameter type (`list[str]` is rejected for `list[object]`); `assert_never` fails on a new enum member; `@override` fails on a typo and `explicit-override` makes it mandatory; `ParamSpec` keeps a keyword-only signature.
- The `from __future__ import annotations` note and the 3.14 lazy-annotation default (PEP 649, 749) come from the Python documentation and were not run here.
- Strict-mode adoption is rewritten around a shrinking override list; the pyright variant comes from its configuration documentation and was not run here.
