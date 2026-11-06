---
type: regex
target: "last_message"
pattern: "mutat[^\\n]{0,80}(argument|input|parameter|caller|rows)|in[- ]place|side effect"
flags: i
weight: 1
---

Names: mutates its argument
