---
type: regex
target: "last_message"
pattern: "\\.get\\(\\s*[\\\"']name|mask[^\\n]{0,40}missing|missing[^\\n]{0,60}(silent|default|empty)|required (field|key)"
flags: i
weight: 1
---

Names: masked missing data (.get with a default)
