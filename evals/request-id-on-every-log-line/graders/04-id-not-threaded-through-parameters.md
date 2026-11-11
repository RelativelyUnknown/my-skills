---
type: regex
target:
  source: file
  path: "src/svc/service.py"
pattern: "def audit\\([^)]*request_id"
match: not_contains
weight: 1
---

audit does not take the id as a parameter
