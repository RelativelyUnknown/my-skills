---
tags: [development, workflow, deprecation]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`parse_ts` is a hand-rolled ISO timestamp parser; `datetime.fromisoformat` does the same job on 3.11+. We don't want it any more. Get rid of it.
