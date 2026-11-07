---
tags: [making-calls-resilient, retries]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `fetch_status(url)` to `src/client/api.py`: GET the URL with httpx and return the parsed JSON. The service is flaky: it sometimes drops the connection, answers 503, or answers 429 with a `Retry-After` header. Make the call resilient, and add tests that run instantly.
