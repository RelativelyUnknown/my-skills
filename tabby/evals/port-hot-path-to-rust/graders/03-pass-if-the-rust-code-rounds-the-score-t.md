---
type: llm
focus:
  source: file
  path: "src/lib.rs"
weight: 3
---

PASS if the Rust code rounds the score to one decimal with ties to even, as Python's round() does (for example round_ties_even applied to score * 10.0 then divided by 10.0, or an equivalent), and does this BEFORE sorting so that items equal after rounding keep their input order. FAIL if it uses f64::round (half away from zero) or sorts on the unrounded score.
