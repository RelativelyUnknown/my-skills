---
type: llm
focus: trace
weight: 2
---

PASS if the agent adds a test asserting 16.99 (or an equivalent half-up case) and observes it failing before it edits `src/pricing/discount.py`. FAIL if the source is changed first and the test is written afterwards, or if the failure is never observed.
