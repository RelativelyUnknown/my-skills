---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "\\bAny\\b"
match: not_contains
weight: 2
---

No `Any`
