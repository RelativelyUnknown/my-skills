---
type: regex
target: "last_message"
pattern: "create_task[^\\n]{0,140}(reference|garbage|collect|discard|lost|exception|await)|RUF006|fire-and-forget|dangling"
flags: i
weight: 1
---

Names: detached asyncio task
