---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `confirm_reset` compares the supplied token (`request.json.get('token')`, which is `None` when omitted) with `user.reset_token`, which is `None` for a user with no pending reset, so `None == None` lets anyone set that user's password by knowing the email. FAIL if it only says the token comparison is not constant-time or misses the None case.
