---
type: regex
target:
  source: file
  path: "src/acme/settings.py"
pattern: "timeout_seconds[^\\n]*=\\s*30[\\s\\S]*retries[^\\n]*=\\s*3|retries[^\\n]*=\\s*3[\\s\\S]*timeout_seconds[^\\n]*=\\s*30"
weight: 1
---

The defaults are literals (30 and 3) where they are declared
