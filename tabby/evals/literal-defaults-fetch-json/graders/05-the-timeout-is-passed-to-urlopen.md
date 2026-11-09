---
type: regex
target:
  source: file
  path: "src/api/client.py"
pattern: "urlopen\\([^)]*timeout\\s*="
weight: 1
---

The timeout is passed to `urlopen`
