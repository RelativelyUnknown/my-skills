---
type: regex
target:
  source: file
  path: "AGENTS.md"
pattern: "kind:.*library/native"
weight: 3
flags: i
arm: with-only
---

`kind:` points at the native library folder
