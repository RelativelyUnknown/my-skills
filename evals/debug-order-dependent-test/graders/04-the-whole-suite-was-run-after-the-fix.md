---
type: llm
focus: trace
weight: 2
---

PASS if, after editing the source, the agent ran the whole suite (not a single test) and the final message reports that result. FAIL if only the single test was run after the fix, or nothing was run.
