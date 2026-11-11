---
tags: [development, senior, ladder]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `slugify(title)` to `src/blog/slug.py`: lowercase, ASCII only (accents dropped, so "Crème brûlée!" becomes "creme-brulee"), words joined by single hyphens, no leading or trailing hyphen. Someone suggested the `python-slugify` package; use your judgement. Add tests.
