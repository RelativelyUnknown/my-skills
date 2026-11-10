---
type: regex
target:
  source: file
  path: "load_orders.py"
pattern: "commit\\(\\)|with conn|BEGIN"
weight: 1
---

Writes are committed in a transaction
