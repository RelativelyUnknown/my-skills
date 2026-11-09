---
type: regex
target:
  source: file
  path: "src/orders/core.py"
pattern: "def \\w*(?:pric|total|discount|subtotal|quote|cost)\\w*\\("
flags: i
weight: 2
---

A pure pricing function exists
