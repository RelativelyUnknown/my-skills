---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "max_workers\\s*=\\s*10|Semaphore\\(\\s*10|\\b[A-Za-z_]*(?:WORKERS|workers|LIMIT|limit|CONCURRENCY|concurrency)[A-Za-z_]*\\s*=\\s*10\\b"
weight: 2
---

Concurrency is capped at 10
