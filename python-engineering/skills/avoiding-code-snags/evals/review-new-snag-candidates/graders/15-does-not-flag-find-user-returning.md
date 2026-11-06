---
type: regex
target: "last_message"
pattern: "find_user[^\\n]{0,140}(should|wrong|bad|snag|problem|swallow|silent|raise instead)|KeyError[^\\n]{0,100}(should|wrong|bad|snag|problem|swallow|silent)"
flags: i
match: not_contains
weight: 2
---

Does not flag: find_user returning None on KeyError
