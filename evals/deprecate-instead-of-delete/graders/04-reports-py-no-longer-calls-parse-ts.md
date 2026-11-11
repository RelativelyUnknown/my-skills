---
type: regex
target:
  source: file
  path: "src/tinydates/reports.py"
pattern: "parse_ts\\("
match: not_contains
weight: 1
---

reports.py no longer calls parse_ts
