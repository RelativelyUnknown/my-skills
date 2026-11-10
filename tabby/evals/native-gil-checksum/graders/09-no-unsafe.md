---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "\\bunsafe\\b"
match: not_contains
weight: 1
---

No unsafe block
