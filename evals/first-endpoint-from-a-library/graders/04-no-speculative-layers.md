---
type: llm
focus: trace
weight: 2
---

PASS if the change adds only what was asked: the endpoint, a way to run it, and tests. FAIL if it also builds an authentication system, a database or ORM layer, a cache, API versioning machinery, or an application settings framework that the request did not call for.
