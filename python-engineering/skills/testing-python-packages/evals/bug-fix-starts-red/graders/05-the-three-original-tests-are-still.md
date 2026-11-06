---
type: regex
target:
  source: file
  path: "tests/test_discount.py"
pattern: "test_zero_percent_returns_price[\\s\\S]*test_full_discount_is_free[\\s\\S]*test_whole_cent_results"
weight: 1
---

The three original tests are still there
