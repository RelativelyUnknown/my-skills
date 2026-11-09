---
tags: [tabby, native, zig]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

Add a `sum_squares(n: u64) -> u64` function to our Ziggy Pydust extension in `src/root.zig`, exposed to Python the same way `fibonacci` already is.
