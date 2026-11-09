---
type: regex
target:
  source: file
  path: "docs/runbooks/stuck-jobs.md"
pattern: "\\b(simply|just|easily|easy|obviously|basically)\\b"
match: not_contains
flags: i
weight: 2
---

The runbook has no minimizers
