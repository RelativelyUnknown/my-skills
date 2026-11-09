---
type: regex
target:
  source: file
  path: "tools/dedupe.py"
pattern: "os\\.replace|\\.replace\\(|NamedTemporaryFile|tempfile"
weight: 2
---

The rewrite is atomic (temporary file, then replace)
