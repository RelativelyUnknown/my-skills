---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "threading\\.Thread\\("
match: not_contains
weight: 1
---

No manual Thread bookkeeping
