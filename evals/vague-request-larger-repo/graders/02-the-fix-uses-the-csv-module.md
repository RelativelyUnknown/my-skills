---
type: regex
target:
  source: file
  path: "src/exporter/formats/csv_format.py"
pattern: "csv\\.(writer|DictWriter)"
weight: 3
---

The fix uses the csv module
