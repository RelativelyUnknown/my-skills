---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "pymodule_export\\]\\s*use super::checksum|wrap_pyfunction!\\(\\s*checksum|add_function"
flags: s
weight: 3
---

checksum is added to the module
