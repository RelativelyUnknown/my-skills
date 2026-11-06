---
type: regex
target:
  source: file
  path: "src/events/when.py"
pattern: "import re\\b|re\\.compile"
match: not_contains
weight: 2
---

No hand-written regex parser
