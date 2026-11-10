---
type: llm
focus: trace
weight: 2
---

PASS if the final message (or a code comment or doc) states the workload it assumed (many hundreds of small ids, per-request sets, set operations) and when the bitset would stop fitting (sparse or unbounded ids, or a very large universe). FAIL if it only says the result is faster.
