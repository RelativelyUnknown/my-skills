---
type: llm
focus: trace
weight: 2
---

PASS if the agent added or kept a test that checks the empty list and the rounding of a half (for example 0.25 becomes 0.2), in addition to the tie order, or a test that compares the Rust result with the Python reference. FAIL if no test covers the empty list or the rounding.
