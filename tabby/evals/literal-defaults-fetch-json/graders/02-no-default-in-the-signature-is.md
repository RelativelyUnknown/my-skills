---
type: regex
target:
  source: file
  path: "src/api/client.py"
pattern: "def fetch_json\\([^)]*=\\s*(?:[A-Za-z_][\\w.]*\\s*[,)]|None)"
match: not_contains
weight: 3
---

No default in the signature is a bare name or None
