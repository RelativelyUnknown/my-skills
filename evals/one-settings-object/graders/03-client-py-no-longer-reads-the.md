---
type: regex
target:
  source: file
  path: "src/shop/client.py"
pattern: "os\\.environ|os\\.getenv"
match: not_contains
weight: 1
---

`client.py` no longer reads the environment
