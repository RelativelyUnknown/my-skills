---
type: regex
target: "last_message"
pattern: "now=datetime|datetime\\.now\\(\\).{0,60}default|default.{0,80}(import time|once|definition)|stamp"
flags: i
weight: 1
---

Names: call in default (datetime.now())
