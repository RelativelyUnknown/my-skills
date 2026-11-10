---
type: regex
target:
  source: file
  path: "src/grid.cpp"
pattern: "out_of_range|index_error|IndexError"
weight: 3
---

An out-of-range index raises instead of reading past the vector
