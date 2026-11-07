---
type: llm
weight: 2
---

PASS if, at some point in the run (a message or the final reply), the assistant tells the user that the `python-project-facts` skill is not installed or could not be run, and that project facts (Python version, runner, tools) are being assumed or defaulted. FAIL if the user is never told, or if the assistant says the facts were detected.
