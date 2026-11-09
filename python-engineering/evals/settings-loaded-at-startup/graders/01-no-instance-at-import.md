---
type: regex
target:
  source: file
  path: "src/app/main.py"
pattern: "^(settings|config|SETTINGS|CONFIG)\\s*(:[^=]+)?=\\s*\\w+\\("
flags: m
match: not_contains
weight: 3
---

No settings object is created at import
