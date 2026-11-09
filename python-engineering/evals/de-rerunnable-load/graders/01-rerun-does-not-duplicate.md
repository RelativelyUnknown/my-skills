---
type: regex
target:
  source: file
  path: "load_orders.py"
pattern: "ON CONFLICT|INSERT OR REPLACE|REPLACE INTO|MERGE|DELETE FROM orders"
flags: i
weight: 4
---

Re-running the same day does not duplicate rows
