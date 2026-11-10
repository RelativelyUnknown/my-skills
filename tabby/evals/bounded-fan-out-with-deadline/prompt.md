---
tags: [development, async, concurrency]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

In `src/crawl/fetch.py`, add `async def fetch_all(urls, fetch_one, limit=10, timeout=5.0)`: call the async function `fetch_one(url)` for every URL concurrently but at most `limit` at a time, return the results in the same order as `urls`, and give up on the whole batch after `timeout` seconds (raise `TimeoutError`, with no call left running). Add tests.
