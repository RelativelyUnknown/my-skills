---
type: regex
target: "last_message"
pattern: "finally[^\\n]{0,140}(return|swallow|discard|mask|hide)|B012"
flags: i
weight: 1
---

Names: return inside finally
