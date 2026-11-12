---
tags: [development, toolstack, guard]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `retry(fn, attempts=3)` to `src/jobkit/retry.py`: it calls `fn` again when it raises `ConnectionError`, up to `attempts` calls in total, and re-raises the last error. Add tests and make sure the checks pass.
