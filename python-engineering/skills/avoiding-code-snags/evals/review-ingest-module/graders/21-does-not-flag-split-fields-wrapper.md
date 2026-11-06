---
type: regex
target: "last_message"
pattern: "_split_fields[^\\n]{0,100}(wrapper|unneeded|unnecessary|inline|remove|delete)"
flags: i
match: not_contains
weight: 2
---

Does not flag: _split_fields wrapper
