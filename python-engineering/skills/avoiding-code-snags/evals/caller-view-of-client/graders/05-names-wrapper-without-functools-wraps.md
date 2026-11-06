---
type: regex
target: "last_message"
pattern: "wraps|ParamSpec|retry.{0,80}(signature|name|docstring)|signature.{0,40}(lost|hid)"
flags: i
weight: 1
---

Names: wrapper without functools.wraps
