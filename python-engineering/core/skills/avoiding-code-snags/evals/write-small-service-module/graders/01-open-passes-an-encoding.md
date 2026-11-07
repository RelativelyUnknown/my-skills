---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "open\\([^)]*encoding\\s*="
weight: 2
---

`open()` passes an encoding
