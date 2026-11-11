---
type: regex
target:
  source: file
  path: "src/catalog/products.py"
pattern: "isinstance\\("
match: not_contains
weight: 2
---

No hand-written type checks
