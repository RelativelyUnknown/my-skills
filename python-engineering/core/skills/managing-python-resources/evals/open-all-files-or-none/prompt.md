---
tags: [managing-python-resources, cleanup]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In `src/files/concat.py`, add `concat(paths, dest)`: open every input file first, all at once, so that a missing or unreadable path fails before anything is written and leaves no file open, then write their contents to `dest` in order. Add tests.
