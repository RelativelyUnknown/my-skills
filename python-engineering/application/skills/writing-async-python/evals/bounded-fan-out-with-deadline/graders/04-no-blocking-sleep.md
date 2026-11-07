---
type: regex
target:
  source: file
  path: "src/crawl/fetch.py"
pattern: "time\\.sleep"
match: not_contains
weight: 1
---

No time.sleep
