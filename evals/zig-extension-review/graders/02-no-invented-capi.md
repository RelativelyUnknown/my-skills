---
type: llm
focus: trace
weight: 2
---

PASS if the agent did not call any CPython C-API functions (PyObject_, Py_, PyArg_) directly. FAIL if it did.
