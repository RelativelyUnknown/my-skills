---
tags: [using-uv, dependencies]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add ruff as a development tool for this project. Also add `scripts/report.py`, a small standalone script that prints a table of the files in `src/` using `rich`; it must run with `uv run scripts/report.py` without making `rich` a dependency of the package.
