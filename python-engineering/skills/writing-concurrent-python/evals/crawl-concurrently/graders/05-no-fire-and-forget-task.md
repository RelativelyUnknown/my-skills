---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "^\\s*asyncio\\.create_task\\("
flags: m
match: not_contains
weight: 1
---

No fire-and-forget task
