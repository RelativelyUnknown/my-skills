---
tags: [development, security]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

A pentest report says our link preview can be made to fetch internal addresses: submitting `http://2130706433/` returned our internal admin page. The preview code is `src/preview/fetch.py`. Fix it and add tests. The tests run with `PYTHONPATH=src python3 -m unittest`.
