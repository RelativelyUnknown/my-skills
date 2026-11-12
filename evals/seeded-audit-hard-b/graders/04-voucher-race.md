---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `vouchers.redeem` checks the balance, calls the partner gateway, and only then reduces the balance, with no lock, transaction or idempotency key, so concurrent requests can redeem the same balance more than once. FAIL if it does not describe the check-then-act race.
