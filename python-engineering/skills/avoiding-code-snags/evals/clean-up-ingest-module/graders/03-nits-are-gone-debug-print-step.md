---
type: regex
target:
  source: file
  path: "src/reports/ingest.py"
pattern: "print\\(|#\\s*Step|#\\s*(?:rows\\.sort|print\\()|^import json|This module ingests"
flags: m
match: not_contains
weight: 1
---

Nits are gone: debug `print`, `# Step`, commented-out code, unused `import json`, narrating docstring
