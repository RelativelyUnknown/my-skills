---
tags: [development, senior, ladder]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

The service has to call the partner's pricing API (`GET https://partner.example/api/prices`) from `src/svc/prices.py`: it must time out, retry on connection errors and 5xx responses with backoff, and reuse connections between calls. Add it, with tests that do not touch the network.
