---
type: regex
target:
  source: file
  path: "static/app.css"
pattern: "font-size:\\s*(?:[0-9]|1[01])px"
match: not_contains
weight: 1
---

No text is set under 12 px
