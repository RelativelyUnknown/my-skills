---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "\\[dependency-groups\\][\\s\\S]*ruff"
weight: 2
---

ruff is in a dependency group
