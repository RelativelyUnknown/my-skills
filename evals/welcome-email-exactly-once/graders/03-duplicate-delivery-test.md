---
type: llm
focus: trace
weight: 2
---

PASS if the agent wrote a test, in any test file under `tests/`, that calls `send_welcome_email` twice for the same user (one after the other or from two threads) and asserts that exactly one email was sent. FAIL if no such test was written.
