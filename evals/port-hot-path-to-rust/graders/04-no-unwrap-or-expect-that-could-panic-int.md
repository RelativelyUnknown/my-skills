---
type: llm
focus: trace
weight: 2
---

PASS if no `.unwrap()`, `.expect(...)`, unchecked indexing or arithmetic in `src/lib.rs` could panic on input a Python caller can supply (an empty list, NaN or infinite scores, very large lists). An `.expect("reason")` or `.unwrap()` on a value the Rust code itself just produced and that cannot fail (for example parsing back a string it formatted from a finite or non-finite `f64`) is fine. FAIL if a caller-supplied value can reach a panic.
