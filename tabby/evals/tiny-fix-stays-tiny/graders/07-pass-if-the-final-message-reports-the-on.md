---
type: llm
focus: last_message
weight: 2
---

PASS if the final message reports the one-word fix and does not make finishing the task depend on the user answering questions. Mentioning in a line or two other things noticed and left alone, or offering a project setup afterwards, is fine. FAIL if the agent asks interview questions instead of fixing the typo, or reports having changed anything besides the typo.
