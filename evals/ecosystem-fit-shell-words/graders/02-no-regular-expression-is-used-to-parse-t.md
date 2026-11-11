---
type: regex
target:
  source: file
  path: "src/runner/cmd.py"
pattern: "re\\.(split|findall|compile)"
match: not_contains
weight: 3
---

No regular expression is used to parse the quoting
