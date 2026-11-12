---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `fetch_rates` (a request to a fixed URL from settings, not caller-controlled) is an SSRF or other vulnerability; a safe note is fine. FAIL if it lists it as a vulnerability.
