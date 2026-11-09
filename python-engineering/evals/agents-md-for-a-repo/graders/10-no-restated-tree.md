---
type: regex
target:
  source: file
  path: "AGENTS.md"
pattern: "```[^`]*(src/tinyq/queue\\.py[^`]*tests/test_queue\\.py|\u251c\u2500\u2500)"
flags: s
match: not_contains
weight: 1
---

Does not paste a file tree
