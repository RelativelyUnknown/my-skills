---
tags: [choosing-python-design-patterns]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Settings are read from `os.environ` in several places. Use the Singleton pattern so the whole app has one settings object it can access. Put the settings code in `src/shop/settings.py`. Keep the tests passing.
