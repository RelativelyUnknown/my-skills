---
type: regex
target: "last_message"
pattern: "timeout.{0,80}(ignored|unused|never|not passed|not used|not forwarded|without)|urlopen\\(url\\)"
flags: i
weight: 1
---

Names: timeout ignored / urlopen without timeout
