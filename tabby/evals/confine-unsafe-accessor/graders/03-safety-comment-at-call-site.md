---
type: llm
focus: trace
weight: 2
---

PASS if any call to the new unchecked accessor is wrapped in an unsafe block with a SAFETY: comment explaining why the precondition holds at that call site. FAIL if the unsafe block has no such comment, or none was added because no call site was written.
