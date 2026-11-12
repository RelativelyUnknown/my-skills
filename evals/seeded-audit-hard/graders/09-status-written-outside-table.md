---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that order status is also written outside the `orders.TRANSITIONS` table, for example the webhook setting `paid` unconditionally (reviving a cancelled order) and/or `jobs.reconcile` marking orders `shipped` regardless of state, so an order can ship without a valid path. FAIL if it only discusses the transition table without the other writers.
