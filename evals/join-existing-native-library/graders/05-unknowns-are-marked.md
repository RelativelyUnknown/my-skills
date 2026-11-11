---
type: regex
target:
  source: file
  path: "AGENTS.md"
pattern: "\\((?:assumed|inferred)\\)"
weight: 2
flags: i
arm: with-only
---

Facts that were inferred or assumed are labelled
