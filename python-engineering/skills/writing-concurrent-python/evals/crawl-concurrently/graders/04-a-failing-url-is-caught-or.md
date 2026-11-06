---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "except|return_exceptions|\\.exception\\(\\)|as_completed"
weight: 2
---

A failing URL is caught or collected per item
