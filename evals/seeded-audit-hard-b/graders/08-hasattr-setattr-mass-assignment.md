---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `accounts.edit` sets any attribute that exists on the patient object (`hasattr`/`setattr`), including `role`, so a patient can make themselves staff or admin (mass assignment). FAIL if it does not name the unrestricted attribute set or the sensitive field.
