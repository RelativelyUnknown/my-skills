---
type: regex
target: "last_message"
pattern: "fetch_text[^\\n]{0,120}(bad|wrong|problem|snag|should)"
flags: i
match: not_contains
weight: 2
---

Does not flag: literal kw-only timeout
