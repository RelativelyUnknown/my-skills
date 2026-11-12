---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `yaml.safe_load` in settings.py is unsafe deserialisation; a safe note is fine. FAIL if it lists it as a vulnerability.
