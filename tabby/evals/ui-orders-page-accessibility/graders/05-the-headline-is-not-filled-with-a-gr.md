---
type: regex
target:
  source: file
  path: "static/app.css"
pattern: "background-clip:\\s*text"
match: not_contains
weight: 1
---

The headline is not filled with a gradient
