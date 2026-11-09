---
type: regex
target:
  source: file
  path: "train.py"
pattern: "StandardScaler\\(\\)\\.fit_transform\\(\\s*df\\["
match: not_contains
weight: 3
---

The scaler is not fit on the whole dataset
