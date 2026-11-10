---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "def \\w+\\([^)]*=\\s*[A-Z][A-Z0-9_]{2,}\\b"
match: not_contains
weight: 2
---

No constant standing in for a default
