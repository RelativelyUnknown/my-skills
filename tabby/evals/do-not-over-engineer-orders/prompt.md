---
tags: [development, architecture, guard]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`process_order` is painful to test. Restructure it so the pricing logic can be tested without mocks and the charge and storage steps can be swapped in tests. Update the tests.
