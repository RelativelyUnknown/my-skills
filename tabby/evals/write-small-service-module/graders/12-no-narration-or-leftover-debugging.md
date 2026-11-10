---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "#\\s*Step\\b|\\bprint\\("
flags: m
match: not_contains
weight: 1
---

No narration or leftover debugging
