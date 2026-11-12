---
type: regex
target: "last_message"
pattern: "ship_order|ship.*(unpaid|without|not paid)|state machine|status transition"
flags: i
weight: 3
---

Reports that an order can ship without being paid
