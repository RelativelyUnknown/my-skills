---
tags: [python-engineering, data-engineering]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

`load_orders.py` runs every night from cron. After a failure we re-ran it and now have duplicate rows for 2026-11-05. Make the job safe to re-run for any day, and let us backfill a range of days. Keep using sqlite3.
