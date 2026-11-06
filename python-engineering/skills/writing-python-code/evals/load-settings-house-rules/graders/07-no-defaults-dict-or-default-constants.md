---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "\\bDEFAULTS?\\b|\\bDEFAULT_[A-Z_]+\\b"
match: not_contains
weight: 2
---

No DEFAULTS dict or DEFAULT_ constants standing in for defaults
