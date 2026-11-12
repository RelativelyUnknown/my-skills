---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "unsafe impl"
match: not_contains
weight: 2
---

No unsafe impl Send or Sync hack
