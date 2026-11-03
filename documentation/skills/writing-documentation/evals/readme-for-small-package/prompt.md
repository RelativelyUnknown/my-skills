---
tags: [writing-documentation]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write a README.md for our package `tinyretry` (a decorator `retry(times=3, backoff_seconds=0.5)` that retries a function on exceptions you pass via `on=(TimeoutError,)`). Install is `pip install tinyretry`, Python 3.11+.
