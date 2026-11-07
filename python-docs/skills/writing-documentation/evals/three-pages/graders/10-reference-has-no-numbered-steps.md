---
type: regex
target:
  source: file
  path: "docs/reference.md"
pattern: "^\\s*\\d+\\. "
flags: m
match: not_contains
weight: 2
---

The reference has no step-by-step instructions
