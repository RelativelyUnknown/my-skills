---
type: regex
target:
  source: file
  path: "train.py"
pattern: "train_test_split\\([^)]*random_state=0\\)"
flags: s
match: not_contains
weight: 1
---

No plain random train_test_split remains
