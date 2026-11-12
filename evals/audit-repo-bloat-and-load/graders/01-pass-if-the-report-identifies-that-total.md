---
type: llm
focus: last_message
weight: 3
---

PASS if the report identifies that `totals_by_customer` runs one query per customer (a query inside a loop, "N+1") and says it will be slow as the customer count grows. FAIL if this is not reported.
