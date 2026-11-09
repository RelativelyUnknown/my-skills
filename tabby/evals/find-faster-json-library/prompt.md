---
tags: [python-engineering]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash, WebFetch, WebSearch]
---

We parse about 2 million JSON Lines events a day with `load_events` in `src/events/load.py`. Is there a faster alternative to the json module that we should use?
