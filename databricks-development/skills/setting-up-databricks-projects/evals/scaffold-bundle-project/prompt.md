---
tags: [setting-up-databricks-projects]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Scaffold a new Databricks project called `shop_etl`: a Python package with one daily job that runs a wheel entry point `load-orders`, deployable to a dev and a prod workspace (host https://adb-123.azuredatabricks.net for both). Create the files.
