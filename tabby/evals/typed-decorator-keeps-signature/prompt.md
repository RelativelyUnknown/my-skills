---
tags: [typing-python-code, annotations]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In `src/util/retry.py`, add a decorator `retry_on(*exceptions, times=3)` that calls the wrapped function again when it raises one of `exceptions`, up to `times` attempts in total. It must be typed for `mypy --strict` so that callers of a decorated function still get their own parameter and return types checked. Add tests.
