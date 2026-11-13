---
type: llm
focus: last_message
weight: 3
---

PASS if the review reports that `payload.len() as u32` silently truncates a payload longer than 4 GiB, so the returned length is wrong, and suggests a checked conversion. FAIL if it is not reported.
