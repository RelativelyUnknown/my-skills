---
type: regex
target: "last_message"
pattern: "tenant[^\\n]{0,140}(key|cache)|(key|cache)[^\\n]{0,140}tenant|cross-tenant"
flags: i
weight: 1
---

Names: cache key omits the tenant
