---
type: regex
target:
  source: file
  path: "tools/dedupe.py"
pattern: "def main\\([^)]*\\)\\s*->\\s*int"
weight: 2
---

`main` returns an int exit code
