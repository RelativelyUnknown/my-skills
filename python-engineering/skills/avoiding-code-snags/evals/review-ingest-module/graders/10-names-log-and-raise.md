---
type: regex
target: "last_message"
pattern: "log[a-z ]*(?:and|then|before)[a-z ,-]*(?:re-?)?raise|double[- ]report|logged and re-?raised"
flags: i
weight: 1
---

Names: log-and-raise
