---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "import re\\b"
match: not_contains
weight: 1
---

No regex
