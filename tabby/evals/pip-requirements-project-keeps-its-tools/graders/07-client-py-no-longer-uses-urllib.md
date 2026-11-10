---
type: regex
target:
  source: file
  path: "src/pricewatch/client.py"
pattern: "urllib"
match: not_contains
weight: 1
---

client.py no longer uses urllib
