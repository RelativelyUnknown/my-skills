---
tags: [development, workers, transactions]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`create_order` in `src/shop/orders.py` saves an order. After an order is created, a worker must send a receipt for it; `enqueue_receipt(order_id)` hands the job to the workers, which run in another process, read the same database, and start a job the moment it is enqueued. Wire the receipt into `create_order`, and run the insert in an explicit transaction. Add a test.
