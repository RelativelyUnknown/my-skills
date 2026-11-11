---
tags: [development, gates, senior]
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Every outbound HTTP call in this repo currently waits forever. Give each one a timeout that defaults to 10 seconds and can be changed with the HTTP_TIMEOUT environment variable, mention the variable in the README, and add a test for the default.
