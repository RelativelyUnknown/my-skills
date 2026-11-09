---
type: regex
target:
  source: file
  path: "src/lib.rs"
pattern: "use super::\\{?[^;]*translate"
flags: s
weight: 3
---

translate is exported from the module
