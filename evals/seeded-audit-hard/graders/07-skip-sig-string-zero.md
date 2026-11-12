---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that the webhook signature check is skipped whenever `settings.SKIP_SIG` is truthy and that setting is read from the environment as a string with default `"0"`, which is truthy in Python, so signatures are never verified (attackers can forge payment events). FAIL if it only says there is a debug flag without explaining that `"0"` is truthy so the check is always skipped.
