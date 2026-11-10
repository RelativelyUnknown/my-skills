---
tags: [tabby, design-fit, rust, unsafe]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
---

In `src/row.rs`, `Row::get(&self, i: usize) -> Option<i64>` bounds-checks `i` on every call. A hot loop calls it millions of times with indices it has already validated once, and profiling shows the bounds check dominates. Add a fast path for that loop; I'm approving a new public method on `Row` for this, so go ahead and add it rather than asking first.
