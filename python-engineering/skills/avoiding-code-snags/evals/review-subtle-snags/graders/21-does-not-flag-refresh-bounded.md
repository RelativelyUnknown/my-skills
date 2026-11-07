---
type: regex
target: "last_message"
pattern: "refresh_bounded[^\\n]{0,160}(should|wrong|bad|problem|unbounded|snag)"
flags: i
match: not_contains
weight: 2
---

Does not flag: refresh_bounded
