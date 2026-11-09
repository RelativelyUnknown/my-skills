---
type: regex
target:
  source: file
  path: "src/client/api.py"
pattern: "429|503|502|504"
weight: 2
---

Retries are tied to transient status codes
