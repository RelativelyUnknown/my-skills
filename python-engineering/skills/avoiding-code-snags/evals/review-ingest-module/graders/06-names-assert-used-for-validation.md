---
type: regex
target: "last_message"
pattern: "\\bassert\\b[^\\n]{0,100}(?:valid|isinstance|-O|stripped)|(?:valid|isinstance|python -O)[^\\n]{0,100}\\bassert\\b"
flags: i
weight: 1
---

Names: assert used for validation
