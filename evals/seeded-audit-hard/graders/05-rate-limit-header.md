---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that the login rate limit is keyed on the client-supplied `X-Forwarded-For` header, so an attacker can change it on every request to avoid the limit (unlimited password guessing). FAIL if it does not say the key comes from a header the client controls.
