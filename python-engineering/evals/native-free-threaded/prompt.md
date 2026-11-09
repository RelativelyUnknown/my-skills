---
tags: [python-engineering, native-extension]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

We want `fastcsv` to run on the free-threaded build of Python 3.14 (`python3.14t`) without the interpreter turning the GIL back on when the module is imported. Make the change. You cannot build here.
