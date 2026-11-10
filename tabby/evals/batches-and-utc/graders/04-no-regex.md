---
type: regex
target:
  source: file
  path: "src/orders/ingest.py"
pattern: "import re\\b"
match: not_contains
weight: 1
---

No regex
