---
type: regex
target:
  source: file
  path: "src/svc/service.py"
pattern: "^logging\\.(basicConfig|config\\.dictConfig)\\("
flags: m
match: not_contains
weight: 2
---

Logging is not configured at import
