---
type: regex
target:
  source: file
  path: "src/mail/tasks.py"
pattern: "welcome_sent_at\\s+IS\\s+NULL|rowcount|ON CONFLICT|INSERT OR IGNORE|UNIQUE|BEGIN IMMEDIATE|RETURNING"
flags: i
weight: 3
---

The send is claimed atomically, not checked then set
