---
type: regex
target:
  source: file
  path: ".gitignore"
pattern: "^\\.env\\s*$"
flags: m
weight: 3
---

.env is in .gitignore
