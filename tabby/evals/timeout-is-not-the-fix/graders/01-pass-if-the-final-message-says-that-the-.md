---
type: llm
focus: last_message
weight: 3
---

PASS if the final message says that the job is slow because `totals_per_customer` runs one query per customer (a query inside a loop, "N+1") and not simply because the timeout is too small. FAIL if it does not identify this.
