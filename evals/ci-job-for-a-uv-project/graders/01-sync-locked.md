---
type: regex
target:
  source: file
  path: ".github/workflows/test.yml"
pattern: "uv sync[^\\n]*--locked"
weight: 3
---

Dependencies are installed with `uv sync --locked`
