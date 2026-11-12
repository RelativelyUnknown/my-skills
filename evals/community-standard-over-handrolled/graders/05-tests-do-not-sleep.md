---
type: regex
target:
  source: file
  path: "tests/test_prices.py"
pattern: "time\\.sleep"
match: not_contains
weight: 1
---

Tests do not sleep
