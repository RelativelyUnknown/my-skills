---
type: regex
target:
  source: file
  path: "src/payments/core.py"
pattern: "^class \\w*(?:Factory|Registry|Manager|Handler|Strategy|Processor)"
flags: m
match: not_contains
weight: 2
---

No Factory, Registry, Manager, Handler, Strategy or Processor class
