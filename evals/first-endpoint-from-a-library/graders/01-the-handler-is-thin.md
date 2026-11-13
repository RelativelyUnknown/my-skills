---
type: llm
focus: trace
weight: 3
---

PASS if the new endpoint calls the existing `lookup_item` for the lookup and holds no copy of that logic (no second normalisation or search written in the handler). FAIL if the lookup logic is reimplemented in the endpoint.
