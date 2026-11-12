---
type: regex
target:
  source: file
  path: "static/app.css"
pattern: "outline:\\s*none"
match: not_contains
weight: 2
---

Keyboard focus is not removed
