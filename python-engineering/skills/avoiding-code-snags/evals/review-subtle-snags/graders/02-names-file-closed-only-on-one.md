---
type: regex
target: "last_message"
pattern: "load_config[^\\n]{0,220}(close|leak|context manager|\\bwith\\b)|(close|leak)[^\\n]{0,220}load_config"
flags: i
weight: 1
---

Names: file closed only on one path
