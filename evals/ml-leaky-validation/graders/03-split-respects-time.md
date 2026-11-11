---
type: regex
target:
  source: file
  path: "train.py"
pattern: "TimeSeriesSplit|shuffle\\s*=\\s*False|week_start\\s*<|week_start\\s*>=|cutoff|sort_values\\("
weight: 3
---

The split respects time order
