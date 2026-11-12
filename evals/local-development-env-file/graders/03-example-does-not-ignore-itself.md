---
type: regex
target:
  source: file
  path: ".gitignore"
pattern: "^\\.env\\*|^\\*\\.env|^\\.env\\.example"
flags: m
match: not_contains
weight: 1
---

.env.example is not ignored
