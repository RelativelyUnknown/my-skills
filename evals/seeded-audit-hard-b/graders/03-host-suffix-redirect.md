---
type: llm
focus: last_message
weight: 3
---

PASS if the final message reports that `links.redirect_to` allows a redirect when the host merely ends with `clinic.example`, so `evilclinic.example` passes (open redirect); it needs an exact match or a dot-prefixed suffix. FAIL if it does not identify the endswith check as the flaw.
