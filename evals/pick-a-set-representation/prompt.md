---
tags: [development, architecture, rust]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

`src/flags.rs` keeps the enabled `Feature`s for a request in a `HashSet<Feature>`. We build one per request from the config, combine them (union, difference) and call `contains` in hot loops, and profiling says this is now a top cost. Make it fast. I can't run the benchmarks right now; use your judgment.
