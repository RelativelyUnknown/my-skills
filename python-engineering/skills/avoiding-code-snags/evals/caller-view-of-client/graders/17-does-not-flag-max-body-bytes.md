---
type: regex
target: "last_message"
pattern: "MAX_BODY_BYTES[^\\n]{0,100}(bad|wrong|inline|problem|snag)"
flags: i
match: not_contains
weight: 2
---

Does not flag: MAX_BODY_BYTES
