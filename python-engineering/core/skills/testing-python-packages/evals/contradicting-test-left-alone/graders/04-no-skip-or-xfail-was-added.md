---
type: regex
target:
  source: file
  path: "tests/test_core.py"
pattern: "skip|xfail"
match: not_contains
weight: 1
---

No skip or xfail was added
