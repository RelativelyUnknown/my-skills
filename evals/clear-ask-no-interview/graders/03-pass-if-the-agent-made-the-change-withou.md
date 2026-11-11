---
type: llm
focus: trace
weight: 3
---

PASS if the agent made the change without first asking the user a question: it read the code and edited it (or wrote the files) before its final message, and its final message does not end with questions the user must answer before the flag works. FAIL if it stopped to ask questions or to run an interview instead of doing the work.
