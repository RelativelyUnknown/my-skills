---
type: regex
target:
  source: file
  path: "src/tinydates/compat.py"
pattern: "DeprecationWarning|FutureWarning|warnings\\.deprecated|@deprecated"
weight: 3
---

It warns that it is deprecated
