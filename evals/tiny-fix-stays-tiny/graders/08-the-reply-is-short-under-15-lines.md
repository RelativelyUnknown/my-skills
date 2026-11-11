---
type: regex
target: "last_message"
pattern: "(?:[^\\n]*\\n){15}"
match: not_contains
weight: 1
---

The reply is short (under 15 lines)
