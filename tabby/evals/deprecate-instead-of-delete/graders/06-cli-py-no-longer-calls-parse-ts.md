---
type: regex
target:
  source: file
  path: "src/tinydates/cli.py"
pattern: "parse_ts\\("
match: not_contains
weight: 1
---

cli.py no longer calls parse_ts
