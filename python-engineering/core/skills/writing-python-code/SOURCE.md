# Sources

`references/errors-and-validation.md` is adapted from two skills of one upstream. The rest of this skill is original to this repository.

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-error-handling/` and `plugins/python-development/skills/python-code-style/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream licence is kept as `LICENSE.wshobson` and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- `python-error-handling` (193 + 171 lines): condensed to one reference of three sections. Kept in rewritten form: validate and convert to domain types at the edge, exception chaining, and batch processing with partial failures. Dropped because `SKILL.md` already covers them or they are library tutorials: the pydantic validation walkthrough, the exception-hierarchy listing, the status-code mapping and the progress-reporting example.
- `python-code-style` (360 lines): not folded in beyond a pointer. It is a formatter, linter and naming tutorial; the project's formatter and linter own style, and the docstring conventions are covered by `python-docs`. Nothing from it is copied.
- New, run on Python 3.13: `raise ... from` keeps `__cause__`; `add_note` appears in `__notes__`; `ExceptionGroup` with `except*` handles a batch's failures by type. The three example blocks run as written.
