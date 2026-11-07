---
tags: [running-background-jobs, transactions]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`create_order` in `src/shop/orders.py` saves an order, and a worker must send a receipt for it with `enqueue_receipt(order_id)`. Workers run jobs the moment they are enqueued, in another process that reads the database. Change `create_order` so it runs the insert in an explicit transaction and so the worker can never see the job before the order is committed. Add a test.
