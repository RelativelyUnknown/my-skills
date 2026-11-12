---
type: regex
target:
  source: file
  path: "tests/test_compat.py"
pattern: "deprecated_call|pytest\\.warns|catch_warnings"
weight: 2
---

A test checks the warning
