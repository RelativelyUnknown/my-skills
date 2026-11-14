---
type: llm
focus: trace
weight: 2
---

PASS if the same test cases run against the fake and against the real PaymentGateway (one parametrized fixture or shared test body), so a difference between them would fail a test. FAIL if the fake has tests only of itself, or the real gateway is never exercised.
