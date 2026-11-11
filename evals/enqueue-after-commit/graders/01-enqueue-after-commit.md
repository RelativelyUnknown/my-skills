---
type: llm
focus:
  source: file
  path: "src/shop/orders.py"
weight: 3
---

PASS if `enqueue_receipt` is called only after the transaction that inserts the order has committed (after the `with conn:` / commit statement, or through an on-commit hook or an outbox written in the same transaction). FAIL if it is called inside the open transaction or before the commit.
