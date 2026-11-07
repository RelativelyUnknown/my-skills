---
type: regex
target: "last_message"
pattern: "session[^\\n]{0,140}(shared|concurrent|gather|not (thread|task|concurrency)[- ]safe|one session|same session)"
flags: i
weight: 1
---

Names: one session shared by concurrent tasks
