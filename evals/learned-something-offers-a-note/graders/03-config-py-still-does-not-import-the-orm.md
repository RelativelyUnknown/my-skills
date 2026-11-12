---
type: regex
target:
  source: file
  path: "src/app/config.py"
pattern: "app\\.orm|from app import orm|import orm"
match: not_contains
weight: 3
---

config.py still does not import the ORM
