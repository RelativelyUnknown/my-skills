---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "\\.get\\(\\s*[\\\"']region"
match: not_contains
weight: 1
---

`region` is not read with `.get`
