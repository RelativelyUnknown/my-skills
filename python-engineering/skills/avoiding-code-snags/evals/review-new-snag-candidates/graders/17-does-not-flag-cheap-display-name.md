---
type: regex
target: "last_message"
pattern: "display_name[^\\n]{0,140}(should|wrong|bad|snag|problem|I/O)"
flags: i
match: not_contains
weight: 2
---

Does not flag: cheap display_name property
