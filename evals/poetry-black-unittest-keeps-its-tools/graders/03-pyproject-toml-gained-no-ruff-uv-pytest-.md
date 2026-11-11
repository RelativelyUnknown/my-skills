---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "\\[tool\\.ruff|\\[tool\\.uv|\\[tool\\.pytest|\\[project\\]"
match: not_contains
weight: 3
---

pyproject.toml gained no ruff, uv, pytest or PEP 621 [project] configuration
