---
type: regex
target:
  source: file
  path: "tests/test_orders.py"
pattern: "(patch|Mock|MagicMock|create_autospec)\\([^)]*Inventory"
match: not_contains
weight: 1
---

The agent's own Inventory is never patched or mocked
