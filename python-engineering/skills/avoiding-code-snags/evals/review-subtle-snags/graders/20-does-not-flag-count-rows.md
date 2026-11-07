---
type: regex
target: "last_message"
pattern: "count_rows[^\\n]{0,140}(should|wrong|bad|problem|snag|leak|never closed)"
flags: i
match: not_contains
weight: 2
---

Does not flag: count_rows
