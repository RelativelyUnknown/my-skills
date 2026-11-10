---
tags: [development, senior, ecosystem]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add `parse_command(line)` to `src/runner/cmd.py`: split a command line the user typed into its arguments the way a shell would, so that `git commit -m "fix the bug"` gives four arguments and not six. Add tests.
