---
type: regex
target: "last_message"
pattern: "\\bconfirmed\\b[\\s\\S]*needs[ _-]validation|needs[ _-]validation[\\s\\S]*\\bconfirmed\\b"
flags: i
weight: 1
arm: with-only
---

Uses the skill's bucket names (confirmed, needs validation); indicator only
