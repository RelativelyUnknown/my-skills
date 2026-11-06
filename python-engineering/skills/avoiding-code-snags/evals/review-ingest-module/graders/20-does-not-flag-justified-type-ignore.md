---
type: regex
target: "last_message"
pattern: "type:\\s*ignore[^\\n]{0,100}(remove|unjustified|bad|snag|problem|wrong|should)"
flags: i
match: not_contains
weight: 2
---

Does not flag: justified type: ignore
