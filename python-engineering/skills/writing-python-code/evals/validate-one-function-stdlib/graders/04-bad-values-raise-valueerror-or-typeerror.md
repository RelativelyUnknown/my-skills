---
type: regex
target:
  source: file
  path: "src/shop/pricing.py"
pattern: "raise (?:ValueError|TypeError)"
weight: 1
---

Bad values raise ValueError or TypeError
