---
type: regex
target:
  source: file
  path: "tests/test_api.py"
pattern: "time\\.sleep\\("
match: not_contains
weight: 2
---

Tests do not call time.sleep
