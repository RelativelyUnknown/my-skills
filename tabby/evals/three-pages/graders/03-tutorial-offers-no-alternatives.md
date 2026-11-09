---
type: regex
target:
  source: file
  path: "docs/tutorial.md"
pattern: "alternatively|you can also|another option|other options|if you prefer"
flags: i
match: not_contains
weight: 2
---

The tutorial offers no choices or alternatives
