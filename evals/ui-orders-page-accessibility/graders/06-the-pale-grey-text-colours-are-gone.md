---
type: regex
target:
  source: file
  path: "static/app.css"
pattern: "#bbbbbb|#aaaaaa|#bbb\\b|#aaa\\b"
flags: i
match: not_contains
weight: 2
---

The pale grey text colours are gone
