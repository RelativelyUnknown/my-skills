---
type: regex
target: "last_message"
pattern: "async[^\\n]{0,120}(block|time\\.sleep|urlopen)|(block|time\\.sleep|urlopen)[^\\n]{0,120}async|event loop"
flags: i
weight: 1
---

Names: blocking call inside async def
