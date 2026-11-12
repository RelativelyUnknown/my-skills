---
type: llm
focus: trace
weight: 3
---

PASS if the new unsafe fn has a doc comment with a Safety section (or equivalent, e.g. "# Safety") stating the precondition the caller must uphold (the index must be in bounds / less than len()). FAIL if the function has no stated precondition.
