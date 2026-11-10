---
type: regex
target:
  source: file
  path: "docs/architecture.svg"
pattern: "#004A96|#4472AA|#7CA0C6|#E0E9F2|#6FB0FF"
match: not_contains
weight: 3
---

No default accent colour is left in the SVG
