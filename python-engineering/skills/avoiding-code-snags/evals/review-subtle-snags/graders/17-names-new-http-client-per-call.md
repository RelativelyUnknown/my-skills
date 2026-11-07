---
type: regex
target: "last_message"
pattern: "AsyncClient[^\\n]{0,140}(each|every|per|new|creat|reuse|pool)|connection pool"
flags: i
weight: 1
---

Names: new HTTP client per call
