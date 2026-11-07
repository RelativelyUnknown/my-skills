---
type: regex
target: "last_message"
pattern: "(race|concurrent|interleav|twice|duplicate|both tasks)[^\\n]{0,140}(await|load|miss)|check-then-act|await[^\\n]{0,120}(race|another task|other task)"
flags: i
weight: 1
---

Names: check-then-act across an await
