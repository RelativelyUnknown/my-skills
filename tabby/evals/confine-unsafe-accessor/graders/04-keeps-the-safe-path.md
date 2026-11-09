---
type: llm
focus: trace
weight: 2
---

PASS if Row::get (the safe, checked accessor) is kept working and used by everything except the identified hot loop. FAIL if the safe accessor was removed or the whole struct was made unsafe-only.
