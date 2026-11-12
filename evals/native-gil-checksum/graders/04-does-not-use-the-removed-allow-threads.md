---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "allow_threads"
match: not_contains
weight: 2
---

Does not use the removed allow_threads
