---
type: regex
target:
  source: file
  path: "docs/troubleshooting.md"
pattern: "\\b(simply|just|easily|easy|obviously|basically)\\b"
match: not_contains
flags: i
weight: 1
---

The troubleshooting page has no minimizers
