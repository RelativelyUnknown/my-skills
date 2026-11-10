---
type: llm
focus: trace
weight: 3
---

PASS if the code either sizes the array from the number of Feature variants at compile time, or checks (assert, debug_assert, const assertion, compile error) that every feature id fits, so adding variants past the size fails loudly instead of silently dropping a flag. FAIL if a larger enum would silently index out of bounds or wrap, or the size is a magic number with no check.
