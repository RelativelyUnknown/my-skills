---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "strict-markers|strict\\s*=\\s*true"
weight: 1
---

pytest options are strict
