---
type: regex
target:
  source: file
  path: "src/exporter/formats/json_format.py"
pattern: "ensure_ascii=False,\\s*\\n\\s*indent=2,"
weight: 1
---

The JSON writer is untouched
