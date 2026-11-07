---
type: regex
target: "last_message"
pattern: "\\bis\\b[^\\n]{0,60}(literal|identity|string)|F632|== ?[\\\"']ready|identity"
flags: i
weight: 1
---

Names: identity compared with a string literal
