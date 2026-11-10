---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "^\\s*assert\\b"
match: not_contains
weight: 1
---

No `assert` as validation
