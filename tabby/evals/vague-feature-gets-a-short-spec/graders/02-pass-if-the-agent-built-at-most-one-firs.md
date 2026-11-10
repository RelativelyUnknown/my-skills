---
type: llm
focus: trace
weight: 3
---

PASS if the agent built at most one first slice (for example a function that builds the email message from the report, with a test) or built nothing, and did not build an entire feature at once (scheduler, SMTP sending, configuration and templates together). FAIL if it implemented the whole feature on unconfirmed assumptions.
