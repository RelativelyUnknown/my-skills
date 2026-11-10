---
tags: [development, uv, ci]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `.github/workflows/test.yml` that runs the tests of this project on every pull request. The project uses uv and has a committed `uv.lock`.
