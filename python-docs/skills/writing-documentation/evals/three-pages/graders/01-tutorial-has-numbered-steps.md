---
type: regex
target:
  source: file
  path: "docs/tutorial.md"
pattern: "^\\s*2\\.\\s|^#{1,4}\\s*(Step\\s*)?2\\b"
flags: m
weight: 2
---

The tutorial is one numbered path (at least two steps)
