---
tags: [development, architecture, rust, unsafe]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

`src/row.rs`: `Row::get` is called millions of times per query in a loop over indices we have already validated, and profiling says its bounds check is now the top cost. Make it fast. I can't run the benchmarks right now; use your judgment. A new public method on `Row` is approved, so go ahead.
