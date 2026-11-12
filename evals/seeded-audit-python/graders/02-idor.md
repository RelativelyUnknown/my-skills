---
type: regex
target: "last_message"
pattern: "get_invoice|/invoice|idor|owner check|insecure direct object"
flags: i
weight: 3
---

Reports the missing owner check in get_invoice
