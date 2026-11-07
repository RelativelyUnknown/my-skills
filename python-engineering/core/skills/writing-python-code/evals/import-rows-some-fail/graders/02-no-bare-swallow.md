---
type: regex
target:
  source: file
  path: "src/ledger/importer.py"
pattern: "except[^\\n]*:\\s*\\n\\s*(pass|continue)\\b"
match: not_contains
weight: 2
---

No except block that only passes or continues
