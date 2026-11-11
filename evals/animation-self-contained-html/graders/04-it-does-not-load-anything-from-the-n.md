---
type: regex
target:
  source: file
  path: "docs/webhook-flow.html"
pattern: "<script[^>]*\\ssrc=|<link[^>]*href=\"https?:|@import\\s+url\\([\"\\']?https?:"
match: not_contains
weight: 2
---

It does not load anything from the network
