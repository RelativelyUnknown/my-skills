---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `verify_otp` compares the supplied `code` (`None` when omitted) with `patient.pending_otp`, which is `None` when no code is pending, so `None == None` issues a token for anyone who knows a phone number. FAIL if it only says the comparison is not constant-time or misses the None case.
