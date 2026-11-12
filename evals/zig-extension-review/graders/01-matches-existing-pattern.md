---
type: llm
focus: trace
weight: 3
---

PASS if the new sum_squares function uses the same style as fibonacci: a Zig function taking a struct-shaped args parameter, registered implicitly via the existing comptime py.rootmodule(@This()) block (no new boilerplate module-init code invented). FAIL if it writes raw CPython C-API calls or invents a different registration mechanism not present in the file.
