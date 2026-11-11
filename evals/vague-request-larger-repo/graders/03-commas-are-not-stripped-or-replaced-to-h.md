---
type: regex
target:
  source: file
  path: "src/exporter/formats/csv_format.py"
pattern: "\\.replace\\(\\s*[\\\"'],[\\\"']"
match: not_contains
weight: 2
---

Commas are not stripped or replaced to hide the problem
