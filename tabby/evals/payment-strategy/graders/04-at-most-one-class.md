---
type: regex
target:
  source: file
  path: "src/payments/core.py"
pattern: "^class [\\s\\S]*^class "
flags: m
match: not_contains
weight: 1
---

At most one class
