---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "\\.get\\([^)]*,\\s*(?:0|1|1\\.0|\\\"\\\"|'')\\)"
match: not_contains
weight: 2
---

No masked missing data: `.get(` with a fallback on required fields
