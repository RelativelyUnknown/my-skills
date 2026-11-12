---
type: regex
target:
  source: file
  path: "src/csvstat/main.py"
pattern: "/home/dev"
match: not_contains
weight: 3
---

The hard-coded personal path is gone
