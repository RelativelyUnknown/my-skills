---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "ThreadPoolExecutor|asyncio|concurrent\\.futures"
weight: 1
---

Uses a standard concurrency tool
