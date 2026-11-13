---
tags: [development, debugging]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`tests.test_defaults.DefaultsTest.test_default_usd_rate` passes when I run it on its own but fails when I run the whole suite (`python3 -m unittest`; the code lives under `src/`, so use `PYTHONPATH=src`). CI is red because of it. Please sort it out.
