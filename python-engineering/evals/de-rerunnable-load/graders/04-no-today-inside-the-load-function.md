---
type: regex
target:
  source: file
  path: "load_orders.py"
pattern: "def (load|run)\\w*\\([^)]*\\):[^\\n]*\\n(?:[ \\t]+[^\\n]*\\n)*?[ \\t]+[^\\n]*(date\\.today\\(|datetime\\.now\\()"
match: not_contains
weight: 2
---

The load function does not call the clock
