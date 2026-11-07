---
tags: [writing-python-code]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `fetch_json(url)` to `src/api/client.py`: GET a URL and return the parsed JSON, with a timeout and a retry on connection errors. Make the timeout and the retry count easy to change later. Use only the standard library.
