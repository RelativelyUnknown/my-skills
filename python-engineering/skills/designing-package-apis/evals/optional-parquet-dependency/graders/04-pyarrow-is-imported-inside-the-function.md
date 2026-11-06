---
type: regex
target:
  source: file
  path: "src/reports/export.py"
pattern: "^\\s+(?:import pyarrow|from pyarrow)"
flags: m
weight: 1
---

pyarrow is imported inside the function
