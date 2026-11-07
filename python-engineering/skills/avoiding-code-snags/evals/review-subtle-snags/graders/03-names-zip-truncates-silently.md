---
type: regex
target: "last_message"
pattern: "zip[^\\n]{0,120}(truncat|strict|length|silently)|strict=True"
flags: i
weight: 1
---

Names: zip truncates silently
