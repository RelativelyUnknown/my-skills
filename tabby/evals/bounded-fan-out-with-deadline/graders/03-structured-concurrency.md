---
type: llm
focus:
  source: file
  path: "src/crawl/fetch.py"
weight: 2
---

PASS if, when the deadline passes or one call raises, no `fetch_one` call is left running in the background: the calls run in an `asyncio.TaskGroup`, or the code cancels the remaining tasks and awaits them before returning or raising. FAIL if tasks are created with `create_task` or passed to a plain `gather` and nothing cancels the others on timeout or failure.
