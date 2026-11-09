---
type: regex
target:
  source: file
  path: "src/client/api.py"
pattern: "while\\s+True"
match: not_contains
weight: 1
---

No unbounded loop
