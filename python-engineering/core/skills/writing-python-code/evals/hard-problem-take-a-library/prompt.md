---
tags: [writing-python-code, dependencies, guard]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `parse_when(text)` in `src/events/when.py`. Users type dates in free form, for example '3rd of March 2026', 'tomorrow 5pm' or '2026-03-03 17:00 CET'. Return a timezone-aware datetime.
