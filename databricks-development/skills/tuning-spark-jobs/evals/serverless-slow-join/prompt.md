---
tags: [tuning-spark-jobs]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our nightly job on serverless compute went from 10 to 45 minutes. I tried setting spark.sql.shuffle.partitions to 2000 and turning off AQE but it got worse. The main step joins orders (3B rows) to customers (2M rows) and then a Python UDF categorizes amounts. What should I do?
