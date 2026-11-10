---
type: regex
target:
  source: file
  path: "src/textkit/wrap.py"
pattern: "DEFAULT_WIDTH = 72[\\s\\S]*def wrap\\(text, width=DEFAULT_WIDTH\\):"
weight: 3
---

The rest of the function is unchanged: no refactor of the constant or the signature
