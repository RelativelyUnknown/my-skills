---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "\\.unwrap\\(\\)|\\.expect\\("
match: not_contains
weight: 2
---

No unwrap or expect that could panic into Python
