---
type: regex
target:
  source: file
  path: "src/api/client.py"
pattern: "^[A-Z][A-Z0-9_]*(?:TIMEOUT|RETR|ATTEMPT|DEFAULT)[A-Z0-9_]*\\s*="
flags: m
match: not_contains
weight: 2
---

No module constant standing in for a default
