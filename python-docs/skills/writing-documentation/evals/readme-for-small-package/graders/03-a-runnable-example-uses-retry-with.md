---
type: regex
target:
  source: file
  path: "README.md"
pattern: "retry\\([^)]*on=\\(TimeoutError,\\)"
weight: 2
---

A runnable example uses `retry(` with `on=(TimeoutError,)`
