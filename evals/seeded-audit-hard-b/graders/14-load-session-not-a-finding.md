---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `load_session` is unsafe deserialisation without noting the HMAC verified with `compare_digest` before `pickle.loads`; a labelled hardening remark is fine. FAIL if it lists it as a plain pickle vulnerability.
