---
type: regex
target:
  source: file
  path: "train.py"
pattern: "transform\\(\\s*[\\\"']mean[\\\"']\\s*\\)"
match: not_contains
weight: 3
---

The store mean of the target is not computed on all rows
