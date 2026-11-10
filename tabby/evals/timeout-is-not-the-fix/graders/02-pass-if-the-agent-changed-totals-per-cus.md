---
type: llm
focus: trace
weight: 3
---

PASS if the agent changed `totals_per_customer` so it no longer runs one query per customer (a single grouped query or join), with the existing test still passing, OR clearly proposed that change and explained why it did not make it. FAIL if the only change was the timeout number.
