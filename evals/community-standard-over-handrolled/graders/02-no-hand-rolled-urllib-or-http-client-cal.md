---
type: regex
target:
  source: file
  path: "src/svc/prices.py"
pattern: "urllib\\.request|http\\.client"
match: not_contains
weight: 2
---

No hand-rolled urllib or http.client call
