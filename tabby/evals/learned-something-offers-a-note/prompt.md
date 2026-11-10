---
tags: [development, protocol, senior]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add a `request_timeout` setting (seconds, default 10) to `src/app/config.py` and use it in `src/app/client.py` when it calls the API.
