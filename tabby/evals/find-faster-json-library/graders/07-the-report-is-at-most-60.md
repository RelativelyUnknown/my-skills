---
type: regex
target: "last_message"
pattern: "(?:[^\\n]*\\n){61}"
match: not_contains
weight: 1
---

The report is at most 60 lines
