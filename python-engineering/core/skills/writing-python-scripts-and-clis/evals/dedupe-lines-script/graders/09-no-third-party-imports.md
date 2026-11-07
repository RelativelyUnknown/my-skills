---
type: regex
target:
  source: file
  path: "tools/dedupe.py"
pattern: "^(?:import|from) (?:click|typer|rich|requests)\\b"
flags: m
match: not_contains
weight: 1
---

No third-party imports
