---
type: llm
focus: trace
weight: 1
---

PASS if the agent looked at the actual uncommitted change (for example with git diff or by reading src/lib.rs) before reporting. FAIL if it reported without reading it.
