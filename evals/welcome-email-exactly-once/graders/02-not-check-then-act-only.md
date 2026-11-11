---
type: llm
focus:
  source: file
  path: "src/mail/tasks.py"
weight: 2
---

PASS if two concurrent calls for the same user cannot both pass the guard before either records the send (an atomic UPDATE/INSERT decides who sends, or a lock/transaction covers check and set). FAIL if the code reads `welcome_sent_at`, returns when set, and only later writes it in a separate statement.
