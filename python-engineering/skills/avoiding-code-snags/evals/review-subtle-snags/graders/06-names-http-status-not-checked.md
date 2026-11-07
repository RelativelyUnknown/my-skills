---
type: regex
target: "last_message"
pattern: "raise_for_status|status (code|check)|non-2xx|http error|4xx|5xx"
flags: i
weight: 1
---

Names: HTTP status not checked
