---
type: regex
target:
  source: file
  path: "src/reports/export.py"
pattern: "^(?:import pyarrow|from pyarrow)"
flags: m
match: not_contains
weight: 2
---

No top-level pyarrow import
