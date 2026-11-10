---
type: llm
focus: trace
weight: 2
---

PASS if a missing or unreadable input file now gives a short error message and a non-zero exit code instead of a Python traceback. FAIL if the traceback behaviour was left.
