---
type: regex
target:
  source: file
  path: "README.md"
pattern: "pip install|uv add|uv pip install"
weight: 1
---

The README has one install command
