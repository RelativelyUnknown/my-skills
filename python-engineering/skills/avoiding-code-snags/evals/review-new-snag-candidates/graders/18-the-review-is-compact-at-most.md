---
type: regex
target: "last_message"
pattern: "(?:[^\\n]*\\n){36}"
match: not_contains
weight: 1
---

The review is compact (at most 35 lines)
