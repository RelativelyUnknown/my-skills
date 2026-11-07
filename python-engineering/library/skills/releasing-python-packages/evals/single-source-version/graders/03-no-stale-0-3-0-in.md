---
type: regex
target:
  source: file
  path: "src/minilib/__init__.py"
pattern: "0\\.3\\.0"
match: not_contains
weight: 1
---

No stale 0.3.0 in the package
