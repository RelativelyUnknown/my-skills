---
type: regex
target: "last_message"
pattern: "parse_typed[^\\n]{0,120}(bad|wrong|problem|snag|should)"
flags: i
match: not_contains
weight: 2
---

Does not flag: Literal-typed option
