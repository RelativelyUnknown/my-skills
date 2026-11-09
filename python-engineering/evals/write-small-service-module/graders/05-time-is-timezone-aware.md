---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "\\bUTC\\b|timezone\\.utc|tzinfo"
weight: 1
---

Time is timezone-aware
