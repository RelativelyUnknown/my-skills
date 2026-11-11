---
type: regex
target:
  source: file
  path: "docs/order-states.svg"
pattern: "linearGradient|radialGradient|feDropShadow|feGaussianBlur"
match: not_contains
weight: 1
---

No gradients or shadows
