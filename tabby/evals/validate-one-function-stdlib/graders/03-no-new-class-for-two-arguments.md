---
type: regex
target:
  source: file
  path: "src/shop/pricing.py"
pattern: "^class "
flags: m
match: not_contains
weight: 2
---

No new class for two arguments
