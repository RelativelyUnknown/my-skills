---
tags: [configuring-python-applications, settings]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Set up the local-development workflow for this service's settings (`APP_DATABASE_URL`, `APP_API_KEY`, `APP_WORKERS`, `APP_DEBUG`): developers should be able to copy a file to `.env` and fill it in. Make the repository safe for that.
