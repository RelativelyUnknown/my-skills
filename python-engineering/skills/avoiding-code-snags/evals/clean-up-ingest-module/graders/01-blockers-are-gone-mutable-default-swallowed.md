---
type: regex
target:
  source: file
  path: "src/reports/ingest.py"
pattern: "def \\w+\\([^)]*=\\s*(?:\\[\\]|\\{\\})|except Exception:\\s*\\n\\s*pass|utcnow|assert isinstance"
match: not_contains
weight: 3
---

Blockers are gone: mutable default, swallowed exception, `utcnow`, `assert isinstance`
