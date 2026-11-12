---
type: regex
target:
  source: file
  path: "src/payments/core.py"
pattern: "(?:[^\\n]*\\n){61}"
match: not_contains
weight: 1
---

`core.py` stays under 60 lines
