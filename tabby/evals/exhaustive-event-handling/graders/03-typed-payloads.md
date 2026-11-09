---
type: regex
target:
  source: file
  path: "src/shop/events.py"
pattern: "TypedDict|@dataclass|NamedTuple|BaseModel"
weight: 2
---

The payloads have a structured type
