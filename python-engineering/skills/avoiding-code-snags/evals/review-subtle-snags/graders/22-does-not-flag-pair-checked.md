---
type: regex
target: "last_message"
pattern: "pair_checked[^\\n]{0,140}(should|wrong|bad|problem|snag|truncat)"
flags: i
match: not_contains
weight: 2
---

Does not flag: pair_checked
