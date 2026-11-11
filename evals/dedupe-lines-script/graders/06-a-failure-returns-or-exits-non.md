---
type: regex
target:
  source: file
  path: "tools/dedupe.py"
pattern: "return [12]\\b|SystemExit\\([12]\\)|sys\\.exit\\([12]\\)"
weight: 1
---

A failure returns or exits non-zero
