---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `load_state` is unsafe deserialisation without noting that it verifies an HMAC with `compare_digest` before `pickle.loads`; a hardening remark clearly labelled as such is fine. FAIL if it lists it as a plain pickle vulnerability.
