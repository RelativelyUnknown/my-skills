---
type: regex
target:
  source: file
  path: "src/orders/ingest.py"
pattern: "\\bUTC\\b|timezone\\.utc"
weight: 1
---

The datetimes are UTC-aware
