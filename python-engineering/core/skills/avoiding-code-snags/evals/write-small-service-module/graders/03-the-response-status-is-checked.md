---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "raise_for_status|\\.status\\b|getcode\\(\\)|HTTPError"
weight: 2
---

The response status is checked
