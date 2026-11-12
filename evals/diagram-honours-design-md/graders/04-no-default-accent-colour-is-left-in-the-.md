---
type: regex
target:
  source: file
  path: "docs/architecture.svg"
pattern: "#2F5BEA|#7C9BFF|#E8EEFF|#1C2547"
match: not_contains
weight: 3
---

No default accent colour is left in the SVG
