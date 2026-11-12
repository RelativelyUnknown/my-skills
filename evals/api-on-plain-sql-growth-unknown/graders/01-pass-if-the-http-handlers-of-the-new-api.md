---
type: llm
focus: trace
weight: 3
---

PASS if the HTTP handlers of the new API contain no SQL strings and call the existing query functions (or functions in the data-access module). FAIL if SQL is written inside the handlers.
