---
type: llm
focus: trace
weight: 3
---

PASS if the response is built from an explicit response shape (a response model, a dict of named fields) that does not contain `cost_price`, and a test or the reply shows it is absent. FAIL if the Item dataclass is serialised whole (for example `asdict(item)` or `item.__dict__`) so `cost_price` is returned.
