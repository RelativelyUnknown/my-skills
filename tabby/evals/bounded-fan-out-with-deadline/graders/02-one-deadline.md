---
type: regex
target:
  source: file
  path: "src/crawl/fetch.py"
pattern: "asyncio\\.timeout\\(|timeout_at\\(|wait_for\\("
weight: 3
---

One deadline covers the whole batch (asyncio.timeout, timeout_at or wait_for)
