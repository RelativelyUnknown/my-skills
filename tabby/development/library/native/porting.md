# Porting a Python function to native code

A port changes the language, not the behaviour. Ask of the original: what does it do that nobody wrote down? Find that before writing a line of the port, because the quiet parts are where ports go wrong. Decide first that it should be native at all ([architecture.md](architecture.md)); this page starts once it should.

Checked on 10 November 2026 with Python 3.13, rustc and g++ (the arithmetic rows below were run); the build templates are in [`development/assets/native/`](../../assets/native/).

## Method

1. **List the observable behaviour.** Every public function, its inputs, outputs and every way it fails. Include: order of results and how ties break, empty input, `None`, whitespace and case, integer limits, rounding, whether it changes its arguments, and what counts as an error rather than a valid edge case.
2. **Tests first.** Keep the original's tests, one native-side test per original name. With none, write characterization tests from the list and run them against the Python original; for the quiet parts, the original's output is the expected value, because the original is the spec.
3. **Keep the Python original** as the reference behind the same signature ([growth.md](../../../references/growth.md) seam). Tests run both on the same inputs and compare, including the awkward ones.
4. **Design the native API from the behaviour,** not from the original's shape: flat buffers and ids across the boundary, errors as one enum mapped to Python exceptions in one place, no panics or C++ exceptions escaping unconverted ([rust.md](rust.md), [cpp.md](cpp.md), [c.md](c.md)).
5. **A bug in the original is kept.** Keep the behaviour, name it in a test (`test_keeps_original_tie_order`) and in the report, and let the owner decide separately. A port is not the place to fix things silently.
6. **Measure both** on the real input. If the gain is under what justified the work, stop and keep the Python.
7. **Order:** pure functions first, then stateful classes. One function per change.

## Where Python and the target differ

| Python | Rust | C++ |
| --- | --- | --- |
| `-7 // 2` is `-4` (floor) | `-7 / 2` is `-3`; `(-7i64).div_euclid(2)` is `-4` | `-7 / 2` is `-3`; floor by hand |
| `round(2.5)` is `2` (ties to even) | `f64::round` gives `3`; `round_ties_even` gives `2` | `std::round` gives `3`; `std::nearbyint` gives `2` |
| `sorted` is stable | `sort_by` is stable, `sort_unstable_by` is not | `std::stable_sort`, not `std::sort` |
| ints do not overflow | `i64` with `checked_add`, or a big-int type | `int64_t` with an overflow check |
| `str` indexes code points | `&str` indexes bytes; use `chars()` | `std::string` indexes bytes |
| `dict` keeps insertion order | `BTreeMap` or `IndexMap` if order is observable; not `HashMap` | `std::map`, or a vector of pairs |
| exceptions | one error enum with `Display` and `Error` | standard exception types the binding maps |
| `None` | `Option<T>` | `std::optional<T>` |

C and Zig follow the same shape: errors as return values or error unions converted at the binding, an explicit owner for every allocation.

## Report

The behaviour list, which quirks were kept and why, the tests that compare native and reference, the benchmark on real input, and what was not built or run.
