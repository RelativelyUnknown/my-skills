---
type: regex
target:
  source: file
  path: "src/app/main.py"
pattern: "bool\\(\\s*os\\.(environ|getenv)"
match: not_contains
weight: 2
---

DEBUG is not parsed with bool() on the raw string
