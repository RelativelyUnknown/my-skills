---
type: regex
target:
  source: file
  path: "src/pay/gateway.py"
pattern: "half|probe"
flags: i
weight: 2
---

A single probe call is allowed after the cool-down
