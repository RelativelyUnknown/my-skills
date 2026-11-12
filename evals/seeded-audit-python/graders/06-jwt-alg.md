---
type: regex
target: "last_message"
pattern: "whoami|get_unverified_header|\bjwt\b"
flags: i
weight: 3
---

Reports the JWT algorithm taken from the token header
