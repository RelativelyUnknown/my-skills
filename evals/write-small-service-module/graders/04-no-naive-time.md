---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "utcnow\\(\\)|datetime\\.now\\(\\)|datetime\\.today\\(\\)|datetime\\.utcfromtimestamp"
match: not_contains
weight: 2
---

No naive time
