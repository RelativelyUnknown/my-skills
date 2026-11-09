---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `list_orders` (the ORDER BY column checked against an allowlist) is a SQL injection vulnerability; a note that it is safe or a hardening remark is fine. FAIL if it lists it as a vulnerability or finding to fix.
