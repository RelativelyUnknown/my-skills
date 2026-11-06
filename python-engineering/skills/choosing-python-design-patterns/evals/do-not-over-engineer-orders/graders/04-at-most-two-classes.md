---
type: regex
target:
  source: file
  path: "src/orders/core.py"
pattern: "^class [\\s\\S]*^class [\\s\\S]*^class "
flags: m
match: not_contains
weight: 1
---

At most two classes
