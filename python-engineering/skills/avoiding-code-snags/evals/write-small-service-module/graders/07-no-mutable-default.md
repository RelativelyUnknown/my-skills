---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "def \\w+\\([^)]*=\\s*(?:\\[\\]|\\{\\})"
match: not_contains
weight: 2
---

No mutable default
