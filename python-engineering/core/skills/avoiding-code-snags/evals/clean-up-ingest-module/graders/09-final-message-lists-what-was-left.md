---
type: llm
focus: last_message
weight: 1
---

PASS if the final message has a section naming what was left alone (the deliberate `except FileNotFoundError`, the justified `type: ignore`, the `_split_fields` helper, or similar) and why. FAIL if it claims everything was changed or never mentions what was kept.
