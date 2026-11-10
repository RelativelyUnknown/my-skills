---
type: regex
target:
  source: file
  path: "AGENTS.md"
pattern: "^\\s*(runner|python|types)\\s*:\\s*\\S+"
flags: mi
weight: 2
arm: with-only
---

The defaults section has key: value lines
