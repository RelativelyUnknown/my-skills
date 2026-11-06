---
type: regex
target:
  source: file
  path: "src/shop/pricing.py"
pattern: "pydantic|marshmallow|cerberus|voluptuous|BaseModel|import attr"
flags: i
match: not_contains
weight: 3
---

No validation library or model class in the function's module
