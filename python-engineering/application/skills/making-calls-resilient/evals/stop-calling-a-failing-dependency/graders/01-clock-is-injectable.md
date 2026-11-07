---
type: regex
target:
  source: file
  path: "src/pay/gateway.py"
pattern: "clock|monotonic|now\\s*[:=]|time_func"
flags: i
weight: 2
---

Time comes through a clock that tests can replace
