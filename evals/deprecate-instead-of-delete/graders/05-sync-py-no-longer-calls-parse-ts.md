---
type: regex
target:
  source: file
  path: "src/tinydates/sync.py"
pattern: "parse_ts\\("
match: not_contains
weight: 1
---

sync.py no longer calls parse_ts
