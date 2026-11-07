---
type: llm
focus:
  source: file
  path: "tests/test_core.py"
weight: 2
---

PASS if at least one test of the pricing logic uses no `mock`, `Mock` or `patch`. FAIL if every test needs a mock.
