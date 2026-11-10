---
type: llm
focus: trace
weight: 3
---

PASS if the choice about the data layer (keep the plain SQL functions, add a query builder, or add an ORM) is made with reasons tied to this project, and the code is consistent with it: the existing query functions still work, or were migrated with tests. FAIL if an ORM, an async rewrite or a cache was added with no reason from this project, or the existing queries were broken or discarded.
