---
type: llm
focus: trace
weight: 3
---

PASS if the agent identifies that `load_rates` returns and mutates the module-level `_DEFAULTS` dict, so one test's override leaks into later tests, and fixes `src/rates/core.py` so the defaults are no longer mutated (for example by copying the dict). FAIL if it only changes tests, test order or configuration, adds sleeps, retries, a cache reset fixture or a skip, or if the cause is never stated.
