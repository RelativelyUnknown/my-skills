---
tags: [python-engineering]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`process_payment` grows a new branch for every payment type. Crypto is next (1% fee, detail key `wallet`, reference `btc-<wallet>`). Refactor it with the right design pattern so adding a type is easy, and add crypto. Keep the existing tests passing.
