---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `billing.refund` checks the status is paid, calls the payment provider, and only then sets `refunded`, with no lock, transaction or idempotency key, so two concurrent requests can refund the same order twice. FAIL if it does not describe the check-then-act race or double refund.
