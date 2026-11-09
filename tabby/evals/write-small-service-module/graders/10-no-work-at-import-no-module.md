---
type: regex
target:
  source: file
  path: "src/orders/service.py"
pattern: "^(?:\\w+\\s*=\\s*)?(?:open\\(|urllib\\.request|requests\\.|os\\.environ|json\\.load)"
flags: m
match: not_contains
weight: 1
---

No work at import: no module-level open, request or environment read
