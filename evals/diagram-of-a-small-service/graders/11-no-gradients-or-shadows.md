---
type: regex
target:
  source: file
  path: "docs/architecture.svg"
pattern: "linearGradient|radialGradient|feDropShadow|feGaussianBlur"
match: not_contains
weight: 1
arm: with-only
---

No gradients or shadows
