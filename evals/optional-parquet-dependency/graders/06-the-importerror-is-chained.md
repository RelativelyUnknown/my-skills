---
type: regex
target:
  source: file
  path: "src/reports/export.py"
pattern: "raise [^\\n]*from\\b"
weight: 1
---

The ImportError is chained
