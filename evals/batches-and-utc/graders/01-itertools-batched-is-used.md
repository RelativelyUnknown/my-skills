---
type: regex
target:
  source: file
  path: "src/orders/ingest.py"
pattern: "batched|islice"
weight: 1
---

Batching uses the standard library (`itertools.batched`, or an `islice` loop), not a hand-rolled index loop
