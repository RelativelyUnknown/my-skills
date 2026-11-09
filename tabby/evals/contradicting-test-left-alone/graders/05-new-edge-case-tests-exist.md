---
type: regex
target:
  source: file
  path: "tests/test_core.py"
pattern: "empty|punctuation|non[-_ ]?ascii|unicode|leading|trailing"
flags: i
weight: 1
---

New edge-case tests exist
