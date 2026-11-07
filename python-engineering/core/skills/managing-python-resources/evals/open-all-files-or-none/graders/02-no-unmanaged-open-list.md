---
type: regex
target:
  source: file
  path: "src/files/concat.py"
pattern: "\\[\\s*open\\(|\\[\\s*Path\\([^)]*\\)\\.open\\("
match: not_contains
weight: 2
---

No list of bare open() results
