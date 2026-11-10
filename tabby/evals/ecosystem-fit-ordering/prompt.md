---
tags: [development, senior, ecosystem]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `plan(tasks)` to `src/runner/plan.py`: `tasks` maps a task name to the names it depends on. Return the names in an order where every task comes after its dependencies. If there is a cycle, raise an error that names the tasks in it. Add tests.
