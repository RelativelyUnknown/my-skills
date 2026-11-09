---
tags: [python-engineering]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In `ingest(rows)`, save the rows in batches of 100 using `save_batch`, and turn each row's `created` value (ISO 8601, like `2026-11-03T10:00:00Z`) into a timezone-aware UTC `datetime` before saving. Add tests.
