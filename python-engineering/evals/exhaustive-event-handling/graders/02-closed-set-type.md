---
type: regex
target:
  source: file
  path: "src/shop/events.py"
pattern: "Literal\\[|class \\w+\\((Str)?Enum"
weight: 1
---

The kinds are a Literal or an Enum
