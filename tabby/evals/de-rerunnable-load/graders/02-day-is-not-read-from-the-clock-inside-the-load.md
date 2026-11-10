---
type: regex
target:
  source: file
  path: "load_orders.py"
pattern: "def (load|main|run)\\w*\\([^)]*(day|start|since)"
weight: 2
---

The day or range is a parameter of the load
