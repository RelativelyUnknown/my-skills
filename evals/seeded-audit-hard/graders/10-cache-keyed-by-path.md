---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `views.account_summary` caches a per-user response under a key that is only the request path, so the first user's name, email and orders are served to other users. FAIL if it does not identify the missing user in the cache key.
