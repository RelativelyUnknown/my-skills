---
tags: [designing-delta-tables]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write the DDL (`orders.sql`) for a new Unity Catalog table main.sales.orders: about 2 TB, growing daily. Most queries filter on customer_id and order_date. Columns: order_id, customer_id, order_date, amount, currency, status.
