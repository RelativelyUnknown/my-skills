---
type: regex
target:
  source: file
  path: "src/shop/orders.py"
pattern: "with conn|BEGIN|\\.commit\\(\\)|transaction\\.atomic|on_commit"
flags: i
weight: 1
---

An explicit transaction is used
