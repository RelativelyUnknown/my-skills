---
tags: [python-engineering]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `to_parquet(rows, path)` to `src/reports/export.py`, written with pyarrow. The package does not depend on pyarrow today.
