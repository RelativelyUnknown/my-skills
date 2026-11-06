---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "pydantic|attrs|marshmallow|cerberus|voluptuous"
flags: i
match: not_contains
weight: 3
---

No validation library is added to pyproject.toml
