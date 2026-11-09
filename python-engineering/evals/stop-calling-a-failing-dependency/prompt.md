---
tags: [making-calls-resilient, circuit-breaker]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`charge(amount)` in `src/pay/gateway.py` calls a payment provider that sometimes goes down for minutes. While it is down every request waits for the provider to time out and our workers fill up. Change the code so that after 5 consecutive failures it stops calling the provider for 30 seconds and fails immediately instead, then lets one call through to test whether it is back. Add tests that run instantly.
