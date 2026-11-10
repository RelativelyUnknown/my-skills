---
type: regex
target:
  source: file
  path: "src/pay/gateway.py"
pattern: "failures|consecutive|threshold"
flags: i
weight: 1
---

Consecutive failures are counted
