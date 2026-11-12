---
type: regex
target: "last_message"
pattern: "withdraw|\\brace\\b|toctou|double.?spend"
flags: i
weight: 3
---

Reports the read-then-write race in withdraw
