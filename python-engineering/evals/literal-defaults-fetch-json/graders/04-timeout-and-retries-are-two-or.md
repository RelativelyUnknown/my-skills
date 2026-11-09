---
type: regex
target:
  source: file
  path: "src/api/client.py"
pattern: "def fetch_json\\([^)]*=[^)]*="
weight: 1
---

Timeout and retries are two or more parameters with defaults
