---
tags: [development, observability, logging]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Every log line written while a request is handled in `src/svc/service.py`, including the lines written by `audit` in the worker thread, must carry that request's id so we can follow one request through concurrent traffic. Add a `request_id` that `handle_request` sets from a parameter, a logging setup function `configure_logging()` that prints JSON lines with the id, and tests.
