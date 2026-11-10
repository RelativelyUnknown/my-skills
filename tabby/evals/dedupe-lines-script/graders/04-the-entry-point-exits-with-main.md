---
type: regex
target:
  source: file
  path: "tools/dedupe.py"
pattern: "(?:raise SystemExit|sys\\.exit)\\(\\s*main\\("
weight: 1
---

The entry point exits with main's code
