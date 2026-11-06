---
type: regex
target: "last_message"
pattern: "property[^\\n]{0,120}(I/O|network|HTTP|request|slow|fetch|client)|(I/O|network|HTTP|fetch)[^\\n]{0,120}property"
flags: i
weight: 1
---

Names: I/O hidden in a property
