---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "sort_unstable"
match: not_contains
weight: 3
---

The sort is stable (no sort_unstable)
