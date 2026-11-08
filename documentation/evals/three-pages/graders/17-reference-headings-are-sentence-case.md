---
type: regex
target:
  source: file
  path: "docs/reference.md"
pattern: "^#{1,3} [A-Z][a-z]+ [A-Z][a-z]+"
flags: m
match: not_contains
weight: 1
---

The reference headings use sentence case
