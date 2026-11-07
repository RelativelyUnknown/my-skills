---
type: regex
target:
  source: file
  path: "src/catalog/products.py"
pattern: "model_validate|TypeAdapter|Product\\(\\*\\*|Product\\(\\*\\*"
weight: 1
---

`load_products` validates through pydantic
