---
type: regex
target: "last_message"
pattern: "subprocess\\.run[^\\n]{0,140}(check|exit (code|status)|return ?code|ignor|fail)|check=True"
flags: i
weight: 1
---

Names: subprocess exit status ignored
