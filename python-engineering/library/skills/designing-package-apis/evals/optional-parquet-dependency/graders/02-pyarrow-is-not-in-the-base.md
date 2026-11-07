---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "^dependencies\\s*=\\s*\\[[^\\]]*pyarrow"
flags: m
match: not_contains
weight: 2
---

pyarrow is not in the base dependencies
