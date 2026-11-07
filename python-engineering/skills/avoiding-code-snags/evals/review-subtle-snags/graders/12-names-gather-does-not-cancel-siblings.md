---
type: regex
target: "last_message"
pattern: "gather[^\\n]{0,180}(cancel|continue|keep running|fail-fast|keeps? going)|TaskGroup"
flags: i
weight: 1
---

Names: gather does not cancel siblings
