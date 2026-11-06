---
type: regex
target:
  source: file
  path: "README.md"
pattern: "^#{2,}\\s+[A-Z][a-z]+\\s+[A-Z][a-z]+"
flags: m
match: not_contains
weight: 1
---

Headings use sentence case (no two capitalised words in a row after the title)
