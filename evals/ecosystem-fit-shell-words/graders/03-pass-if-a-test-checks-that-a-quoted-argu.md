---
type: llm
focus: trace
weight: 2
---

PASS if a test checks that a quoted argument stays one argument, and one checks an unbalanced quote (which shlex reports as a ValueError) is handled or documented. FAIL if neither is tested.
