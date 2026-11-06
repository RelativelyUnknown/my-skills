---
type: regex
target: "last_message"
pattern: "fetch_report[^\\n]{0,140}(should|wrong|bad|snag|problem)"
flags: i
match: not_contains
weight: 2
---

Does not flag: fetch_report literal timeout
