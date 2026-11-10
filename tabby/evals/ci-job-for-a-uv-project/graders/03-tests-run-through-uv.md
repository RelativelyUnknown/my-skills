---
type: regex
target:
  source: file
  path: ".github/workflows/test.yml"
pattern: "uv run[^\\n]*pytest"
weight: 2
---

pytest runs through `uv run`
