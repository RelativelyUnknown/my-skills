---
type: regex
target:
  source: file
  path: "src/pricewatch/client.py"
pattern: "import httpx|from httpx"
weight: 2
---

client.py uses httpx
