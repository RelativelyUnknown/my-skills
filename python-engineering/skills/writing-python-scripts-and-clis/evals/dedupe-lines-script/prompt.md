---
tags: [writing-python-scripts-and-clis, prototype]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write a script `tools/dedupe.py` that removes duplicate lines from a text file in place, keeping the first occurrence of each line. It takes the file path as an argument, and I want a `--dry-run` that prints what would be removed. Use only the standard library.
