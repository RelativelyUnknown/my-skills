---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not report the `shell=True` or `eval` in tests/test_helpers.py (test-only code with literal inputs) as a vulnerability; a note that they are test-only is fine. FAIL if it lists them as findings to fix.
