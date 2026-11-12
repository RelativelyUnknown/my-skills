---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `accounts.update` lets the client set any attribute that exists on the user object (`vars(user)`), including `is_admin`, `password_hash` and `reset_token` (mass assignment / privilege escalation). FAIL if it does not name the unrestricted allowed set or the sensitive fields.
