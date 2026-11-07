---
type: regex
target:
  source: file
  path: ".github/workflows/test.yml"
pattern: "--frozen|pip install"
match: not_contains
weight: 2
---

No --frozen and no pip install
