---
tags: [development]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Bug report: `apply_discount(19.99, 15)` returns 16.9915 but the docstring says results are rounded to cents, half up. Fix it.
