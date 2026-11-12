---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that the one-time-code attempt limit is keyed on the client-supplied `device_id` cookie, so an attacker can change it each request to try unlimited codes. FAIL if it does not say the key is client-controlled.
