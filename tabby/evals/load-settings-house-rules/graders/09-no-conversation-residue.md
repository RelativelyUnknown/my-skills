---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "as requested|as discussed|per the|now uses|no longer|previously"
match: not_contains
weight: 1
---

No conversation residue
