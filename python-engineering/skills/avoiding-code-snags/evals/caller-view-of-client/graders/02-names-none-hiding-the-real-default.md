---
type: regex
target: "last_message"
pattern: "retries=None|retries or 3|None.{0,50}(sentinel|hid|real default)|\\bor 3\\b"
flags: i
weight: 1
---

Names: None hiding the real default (retries)
