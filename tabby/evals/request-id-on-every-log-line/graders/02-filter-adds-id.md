---
type: regex
target:
  source: file
  path: "src/svc/service.py"
pattern: "logging\\.Filter|addFilter|setLogRecordFactory"
flags: i
weight: 2
---

A Filter or record factory adds the id to every record
