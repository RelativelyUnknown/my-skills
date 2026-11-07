---
type: regex
target: "last_message"
pattern: "(remov|mutat|modif)[^\\n]{0,100}(while|during)[^\\n]{0,40}(iterat|loop)|skips? (an )?(item|element)|iterat[^\\n]{0,80}remov"
flags: i
weight: 1
---

Names: mutating a list while iterating
