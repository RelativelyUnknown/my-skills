---
type: llm
focus: trace
weight: 3
---

PASS if flags.rs (or a new module) now stores the enabled features in a fixed-size bitset or array of integers indexed by the feature id (for example [u64; N] or a bit-packed struct), with contains, union and difference done by bit operations, and no HashSet on the hot path. FAIL if it still uses a HashSet or only tunes the hasher (for example a faster hash function).
