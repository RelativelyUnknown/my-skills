---
type: llm
focus: last_message
weight: 3
---

PASS if the final message states the cause: the CSV writer joins the fields with commas without quoting, so a customer whose name (or another field) contains a comma, a quote or a newline produces extra or shifted columns. FAIL if no cause is stated, or a different cause is given (encoding, rounding, dates, the database).
