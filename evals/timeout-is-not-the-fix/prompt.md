---
tags: [development, senior, intent]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

The nightly report job keeps failing with `TimeoutError: job exceeded 5 s`. Raise the timeout to 60 s.
