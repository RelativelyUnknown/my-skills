---
type: llm
focus:
  source: file
  path: "src/orders/service.py"
weight: 2
---

PASS if `load_orders` hands rows to the caller without returning an iterator over a file that the function has already closed (for example `return csv.reader(f)` inside a `with`). FAIL if it does.
