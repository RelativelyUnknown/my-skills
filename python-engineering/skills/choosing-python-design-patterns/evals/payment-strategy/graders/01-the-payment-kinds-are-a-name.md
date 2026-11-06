---
type: regex
target:
  source: file
  path: "src/payments/core.py"
pattern: "=\\s*\\{\\s*[\\\"']card[\\\"']\\s*:"
weight: 2
---

The payment kinds are a name-to-function mapping
