---
tags: [writing-python-code]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `load_settings(path)` in a new module `src/acme/settings.py`. It reads a TOML file with `region` (one of eu, us, ap; required), `timeout_seconds` (default 30) and `retries` (default 3), and returns the settings. Add tests.
