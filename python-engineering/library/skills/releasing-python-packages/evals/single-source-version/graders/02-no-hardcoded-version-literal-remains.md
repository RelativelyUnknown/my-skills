---
type: regex
target:
  source: file
  path: "src/minilib/__init__.py"
pattern: "__version__\\s*=\\s*[\"\\']\\d+\\.\\d+"
match: not_contains
weight: 2
---

No hardcoded `__version__` literal remains
