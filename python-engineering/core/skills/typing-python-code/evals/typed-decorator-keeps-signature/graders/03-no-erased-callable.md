---
type: regex
target:
  source: file
  path: "src/util/retry.py"
pattern: "Callable\\[\\.\\.\\.,\\s*Any\\]"
match: not_contains
weight: 2
---

No Callable[..., Any]
