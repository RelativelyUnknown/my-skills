---
type: regex
target:
  source: file
  path: "README.md"
pattern: "pip install tinyretry"
match: count:1
weight: 1
---

Exactly one install command
