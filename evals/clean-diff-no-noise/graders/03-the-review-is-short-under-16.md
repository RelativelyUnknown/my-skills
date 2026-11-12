---
type: regex
target: "last_message"
pattern: "(?:[^\\n]*\\n){16}"
match: not_contains
weight: 1
---

The review is short (under 16 lines)
