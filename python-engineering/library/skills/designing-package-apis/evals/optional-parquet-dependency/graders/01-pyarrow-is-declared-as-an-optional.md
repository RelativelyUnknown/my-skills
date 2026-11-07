---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "optional-dependencies[\\s\\S]*pyarrow"
weight: 2
---

pyarrow is declared as an optional dependency
