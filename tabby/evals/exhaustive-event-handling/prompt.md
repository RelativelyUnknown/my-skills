---
tags: [development, typing, annotations]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add type annotations to `src/shop/events.py` for `mypy --strict`. The kinds are `created`, `paid` and `cancelled` (a cancelled event has an `id` and a `reason`); handle all three, and make sure that adding a fourth kind later is caught by the type checker rather than at run time. Add tests.
