---
type: regex
target:
  source: file
  path: "tests/test_discount.py"
pattern: "is not None|assert True"
match: not_contains
weight: 1
---

No weak assertions were added
