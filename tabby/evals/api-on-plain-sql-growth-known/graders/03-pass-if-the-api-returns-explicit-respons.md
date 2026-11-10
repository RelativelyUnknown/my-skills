---
type: llm
focus: trace
weight: 2
---

PASS if the API returns explicit response shapes (dataclasses, TypedDicts, pydantic models or a mapping function) rather than passing raw database rows or tuples straight into the JSON. FAIL otherwise.
