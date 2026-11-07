---
type: regex
target: "last_message"
pattern: "retr[^\\n]{0,160}(idempot|twice|duplicate|double|charge|side effect)|idempot"
flags: i
weight: 1
---

Names: retry repeats a non-idempotent write
