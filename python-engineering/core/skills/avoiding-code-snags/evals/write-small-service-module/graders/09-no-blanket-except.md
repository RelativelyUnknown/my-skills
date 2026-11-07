---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "except\\s+Exception|except\\s*:"
match: not_contains
weight: 2
---

No blanket except
