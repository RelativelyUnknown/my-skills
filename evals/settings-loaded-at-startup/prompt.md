---
tags: [development, configuration, settings]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add configuration to the service in `src/app/main.py`. Settings, from environment variables with the prefix `APP_`: `DATABASE_URL` (required), `API_KEY` (required, a secret), `WORKERS` (an integer, default 2), `DEBUG` (a boolean, default false). A bad deployment must fail at startup with one message that lists every missing or invalid setting. Add tests.
