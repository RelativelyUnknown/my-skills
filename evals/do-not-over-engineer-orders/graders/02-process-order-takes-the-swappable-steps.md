---
type: regex
target:
  source: file
  path: "src/orders/core.py"
pattern: "def process_order\\([^)]*(?:charge|save|store|repo|clock|now|today|gateway|pay)"
flags: i
weight: 2
---

`process_order` takes the swappable steps as parameters
