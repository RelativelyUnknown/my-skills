---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "strict\\s*=\\s*true"
weight: 1
---

mypy runs in strict mode
