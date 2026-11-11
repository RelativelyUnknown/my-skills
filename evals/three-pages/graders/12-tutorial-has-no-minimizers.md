---
type: regex
target:
  source: file
  path: "docs/tutorial.md"
pattern: "\\b(simply|just|easy|easily|powerful|seamless|robust|blazing)\\b"
flags: i
match: not_contains
weight: 1
---

The tutorial has no minimizers or puffery
