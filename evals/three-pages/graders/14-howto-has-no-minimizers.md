---
type: regex
target:
  source: file
  path: "docs/howto-retry-only-some-errors.md"
pattern: "\\b(simply|just|easy|easily|powerful|seamless|robust|blazing)\\b"
flags: i
match: not_contains
weight: 1
---

The howto has no minimizers or puffery
