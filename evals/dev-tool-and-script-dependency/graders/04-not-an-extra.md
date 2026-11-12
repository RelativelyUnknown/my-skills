---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "optional-dependencies[\\s\\S]*ruff"
match: not_contains
weight: 1
---

ruff is not in an extra
