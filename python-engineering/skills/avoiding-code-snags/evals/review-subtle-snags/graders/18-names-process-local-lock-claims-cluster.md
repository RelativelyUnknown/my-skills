---
type: regex
target: "last_message"
pattern: "Lock[^\\n]{0,180}(process|worker|cluster|multiple|thread-safe|local)|(thread-safe|cluster-safe)[^\\n]{0,120}(false|wrong|claim|misleading|not)"
flags: i
weight: 1
---

Names: process-local lock claims cluster safety
