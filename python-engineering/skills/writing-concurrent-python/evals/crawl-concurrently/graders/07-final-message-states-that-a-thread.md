---
type: llm
focus: last_message
weight: 2
---

PASS if the final message states that a thread blocked in `fetch` cannot be cancelled by the five-second limit (the call keeps running), or the code bounds the call itself. FAIL if it claims the five-second limit stops a blocked `fetch` without qualification.
