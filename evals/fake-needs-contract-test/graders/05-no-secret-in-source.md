---
type: regex
target:
  source: file
  path: "tests/test_gateway_contract.py"
pattern: "(sk|tok|key)_[A-Za-z0-9]{12,}"
match: not_contains
weight: 1
---

No literal credential appears in the test file
