---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "\\brich\\b"
match: not_contains
weight: 2
---

rich is not a dependency of the package
