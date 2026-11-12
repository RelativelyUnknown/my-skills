---
type: llm
focus: last_message
weight: 2
---

PASS if the final message mentions the project rule that `app.config` must not import the ORM (enforced by the import isolation test), in a way a future maintainer could note down. FAIL if it does not mention it.
