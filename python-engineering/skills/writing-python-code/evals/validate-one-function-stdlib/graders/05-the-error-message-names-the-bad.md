---
type: regex
target:
  source: file
  path: "src/shop/pricing.py"
pattern: "raise (?:ValueError|TypeError)\\([^)]*(?:\\{(?:price|percent)|%[rs]|!r)"
weight: 2
---

The error message names the bad value
