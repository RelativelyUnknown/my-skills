---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `yaml.safe_load` in `load_templates` is unsafe deserialisation. FAIL if it lists it as a vulnerability.
