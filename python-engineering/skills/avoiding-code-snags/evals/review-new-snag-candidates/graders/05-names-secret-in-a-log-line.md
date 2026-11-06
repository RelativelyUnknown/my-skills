---
type: regex
target: "last_message"
pattern: "token[^\\n]{0,80}(log|repr)|(log|repr)[^\\n]{0,80}token|credential[^\\n]{0,60}log|secret"
flags: i
weight: 1
---

Names: secret in a log line
