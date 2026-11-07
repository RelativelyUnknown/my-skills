---
type: regex
target:
  source: file
  path: "src/pay/gateway.py"
pattern: "class \\w*(Open|Unavailable|Circuit)\\w*\\("
flags: i
weight: 2
---

A distinct exception for the open state
