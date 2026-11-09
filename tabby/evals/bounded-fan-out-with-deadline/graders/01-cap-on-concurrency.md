---
type: regex
target:
  source: file
  path: "src/crawl/fetch.py"
pattern: "Semaphore|Queue\\("
weight: 2
---

Concurrency is capped with a Semaphore or a Queue
