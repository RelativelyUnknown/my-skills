---
type: regex
target:
  source: file
  path: "src/shop/db.py"
pattern: "os\\.environ|os\\.getenv"
match: not_contains
weight: 1
---

`db.py` no longer reads the environment
