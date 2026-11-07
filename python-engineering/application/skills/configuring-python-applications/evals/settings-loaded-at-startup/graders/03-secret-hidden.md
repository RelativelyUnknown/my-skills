---
type: regex
target:
  source: file
  path: "src/app/main.py"
pattern: "SecretStr|repr\\s*=\\s*False"
weight: 2
---

The secret is kept out of repr
