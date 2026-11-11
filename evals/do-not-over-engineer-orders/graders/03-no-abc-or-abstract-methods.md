---
type: regex
target:
  source: file
  path: "src/orders/core.py"
pattern: "\\bimport abc\\b|from abc import|abstractmethod"
match: not_contains
weight: 2
---

No ABC or abstract methods
