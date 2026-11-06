---
type: regex
target: "last_message"
pattern: "len\\([a-z_]+\\)\\s*==\\s*0|truthiness|not rows"
flags: i
weight: 1
---

Names: len(rows) == 0
