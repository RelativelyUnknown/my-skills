---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "except\\s+Exception|except\\s*:"
match: not_contains
weight: 1
---

No blanket except
