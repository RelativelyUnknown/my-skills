---
type: regex
target:
  source: file
  path: "tests/test_orders.py"
pattern: "https?://(?!example\\.(com|test|invalid))[a-z]"
match: not_contains
weight: 1
---

No test calls a real host
