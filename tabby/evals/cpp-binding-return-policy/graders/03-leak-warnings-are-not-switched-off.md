---
type: regex
target:
  source: file
  path: "src/grid.cpp"
pattern: "set_leak_warnings\\(\\s*false"
match: not_contains
weight: 1
---

Leak warnings are not switched off
