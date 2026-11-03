---
tags: [building-data-pipelines]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Write a PySpark job `load_orders.py` that loads one day of orders from the bronze table main.shop.orders_bronze into main.shop.orders_silver (columns order_id, customer_id, amount, status, updated_at, ingest_date). The job takes --run-date. Ops reruns failed days all the time, so reruns must not create duplicates.
