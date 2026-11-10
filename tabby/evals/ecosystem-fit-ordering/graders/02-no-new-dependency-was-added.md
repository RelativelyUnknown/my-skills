---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "networkx|toposort"
match: not_contains
weight: 2
---

No new dependency was added
