---
tags: [testing-pyspark-code]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Set up unit tests for our Spark transforms in src/shop/transforms.py (function `add_vat(df, rate)` adds a vat column = amount * rate). Our pyproject has `[dependency-groups] dev = ["pytest", "pyspark==4.1.1", "databricks-connect~=18.0.0"]`. Create the pyproject changes, a conftest and one test file.
