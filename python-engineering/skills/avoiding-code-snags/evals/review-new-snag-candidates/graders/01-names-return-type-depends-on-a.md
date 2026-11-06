---
type: regex
target: "last_message"
pattern: "as_list|return type[^\\n]{0,60}(depend|change|vary|differ)|returns? (a )?(list|dict)[^\\n]{0,40}(or|depending)|overload"
flags: i
weight: 1
---

Names: return type depends on a flag
