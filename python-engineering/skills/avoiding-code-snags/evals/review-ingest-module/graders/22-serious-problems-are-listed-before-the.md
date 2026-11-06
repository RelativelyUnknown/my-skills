---
type: regex
target: "last_message"
pattern: "^(?:(?!mutable default|rows=\\[\\]|except Exception|swallow|utcnow)[\\s\\S])*?(?:debug print|print\\(|# Step|commented-out)"
flags: i
match: not_contains
weight: 2
---

Serious problems are listed before the nits (no nit appears before the first serious one)
