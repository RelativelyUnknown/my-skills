---
type: llm
focus: last_message
weight: 2
---

PASS if the final message does not claim that `render_receipt` (a Jinja2 environment with autoescape on and a constant template) is an XSS or template-injection vulnerability; a safe note is fine. FAIL if it lists it as a vulnerability.
