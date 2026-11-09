---
type: regex
target:
  source: file
  path: "src/shop/mailer.py"
pattern: "os\\.environ|os\\.getenv"
match: not_contains
weight: 1
---

`mailer.py` no longer reads the environment
