---
type: regex
target:
  source: file
  path: "AGENTS.md"
pattern: "^(?:[^\\n]*\\n){46,}"
match: not_contains
weight: 2
---

Is under 46 lines
