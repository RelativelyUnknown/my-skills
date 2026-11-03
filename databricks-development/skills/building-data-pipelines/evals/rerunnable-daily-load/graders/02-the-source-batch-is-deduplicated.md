---
type: llm
focus: trace
weight: 1
---

The source batch is deduplicated to one row per order_id before a MERGE (latest by updated_at)
