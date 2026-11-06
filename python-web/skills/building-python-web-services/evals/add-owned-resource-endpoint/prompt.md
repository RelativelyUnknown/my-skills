---
tags: [building-python-web-services]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In our FastAPI app (app/main.py has `get_current_user` and an async SQLAlchemy `get_session`; model Order has id, owner_id, total, internal_notes), add `GET /orders/{order_id}` that returns the order. Write the code and tests.
