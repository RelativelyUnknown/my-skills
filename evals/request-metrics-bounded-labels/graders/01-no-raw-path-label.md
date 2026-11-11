---
type: regex
target:
  source: file
  path: "src/api/app.py"
pattern: "labels\\([^)]*\\bpath\\b|\\[\\s*\"[^\"]*\"\\s*,[^]]*\\bpath\\b[^]]*\\]|labelnames=\\([^)]*path"
match: not_contains
weight: 3
---

The raw path is not a label
