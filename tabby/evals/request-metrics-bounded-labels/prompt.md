---
tags: [adding-observability, metrics]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add Prometheus metrics to `handle` in `src/api/app.py` using `prometheus_client`: a request counter and a latency histogram. Paths look like `/orders/123` and `/orders/456`, and we have millions of orders, so think about what you label the metrics with. Add a test.
