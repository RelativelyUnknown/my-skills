---
tags: [managing-python-resources, cleanup]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In `src/runner/stream.py`, add `stream_lines(args, limit_seconds)`: run the command in `args` and yield its output line by line; if it has not finished after `limit_seconds`, stop it and raise `TimeoutError`. Add tests.
