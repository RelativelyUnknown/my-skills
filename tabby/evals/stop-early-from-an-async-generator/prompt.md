---
tags: [writing-async-python, cleanup]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `async def first_match(predicate)` to `src/store/search.py`: iterate the async generator `rows()` from `src/store/rows.py` and return the first row for which `predicate(row)` is true (or `None`). The generator holds a connection that `rows.CLOSED` tracks, so it must be released as soon as `first_match` returns. Add a test that checks `CLOSED`.
