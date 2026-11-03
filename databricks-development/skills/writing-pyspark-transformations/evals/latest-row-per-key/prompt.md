---
tags: [writing-pyspark-transformations]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I have a DataFrame of customer updates with columns customer_id, email, updated_at, ingest_seq. Write a function `latest_customers(df)` in `customers.py` that keeps one row per customer: the most recent one.
