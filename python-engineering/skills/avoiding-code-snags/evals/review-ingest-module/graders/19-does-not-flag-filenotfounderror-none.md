---
type: regex
target: "last_message"
pattern: "FileNotFoundError[^\\n]{0,100}(should|wrong|bad|snag|problem|swallow|silent|raise instead)"
flags: i
match: not_contains
weight: 2
---

Does not flag: FileNotFoundError -> None
