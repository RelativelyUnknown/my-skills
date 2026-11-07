---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "urlopen\\([^)]*timeout\\s*=|requests\\.get\\([^)]*timeout|httpx\\.get\\([^)]*timeout"
weight: 3
---

The network call has a timeout
