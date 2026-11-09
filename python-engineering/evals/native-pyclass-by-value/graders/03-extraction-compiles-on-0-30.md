---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "from_py_object|p:\\s*&\\s*Point|p:\\s*PyRef<|p:\\s*&\\s*Bound<|p:\\s*Bound<"
weight: 4
---

The Point argument is opted in with from_py_object or taken by reference
