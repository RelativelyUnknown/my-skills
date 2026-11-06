---
type: regex
target:
  source: file
  path: "src/fetcher/crawl.py"
pattern: "timeout\\s*=\\s*5|asyncio\\.timeout\\(\\s*5|wait_for\\([^)]*\\b5\\b|\\btimeout\\b[^\\n]*\\b5\\b"
weight: 2
---

A five second bound appears
