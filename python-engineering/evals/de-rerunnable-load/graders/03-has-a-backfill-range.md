---
type: regex
target:
  source: file
  path: "load_orders.py"
pattern: "(start|since|from).{0,200}(end|until|to)"
flags: is
weight: 2
---

A start and end allow a backfill
