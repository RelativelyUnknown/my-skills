---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "#\\[pymodule\\(\\s*gil_used\\s*=\\s*false\\s*\\)\\]"
weight: 4
---

The module is declared #[pymodule(gil_used = false)]
