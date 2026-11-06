---
type: regex
target: "last_message"
pattern: "logger\\.exception|traceback|str\\(e\\)|stack trace"
flags: i
weight: 1
---

Names: error logged without traceback
