---
type: regex
target:
  source: file
  path: ".env.example"
pattern: "sk-[A-Za-z0-9]{10,}|AKIA[0-9A-Z]{12,}|[A-Za-z0-9]{32,}"
match: not_contains
weight: 2
---

No real-looking secret in .env.example
