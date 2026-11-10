# Rust with PyO3 and maturin

Layout choice first: [architecture.md](architecture.md). Keep logic in a crate that does not depend on PyO3, so `cargo test` runs without Python; the binding crate only converts types and maps errors.

## Project files

```toml
# pyproject.toml
[build-system]
requires = ["maturin>=1.9,<2"]
build-backend = "maturin"

[tool.maturin]
python-source = "python"      # python/<pkg>/ holds the Python package
module-name = "<pkg>._core"   # the native module is private
```

```toml
# Cargo.toml
[lib]
name = "_core"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "<pin the minor you tested>", features = ["abi3-py39"] }  # abi3 only if you want one wheel per platform

[profile.release]
lto = "fat"
codegen-units = 1
overflow-checks = true   # integer overflow is a bug, not wrap-around

[lints.rust]
unsafe_op_in_unsafe_fn = "warn"
```

PyO3 changes between minors. Pin the minor and read its changelog on upgrade (the GIL-release call became `detach` in 0.26; extracting a `#[pyclass]` by value needs an explicit opt-in from 0.27).

## Errors

- Every exported function returns `PyResult<T>`. Map each Rust error to the closest Python exception (`ValueError`, `OSError`, the package's root exception) in one `impl From<MyError> for PyErr`. Messages are lowercase, say the bad value and the fix.
- A panic is a bug, not an error path. No `unwrap()` or `expect()` on data from Python or the outside world; use `?`. Reserve `expect("reason")` for invariants your own code guarantees.
- Never let a panic or a C error cross without conversion.

## GIL, threads, ownership

- Release the GIL for long work that touches no Python objects: `py.detach(|| ...)` (the closure must be `Send`).
- Borrow, do not clone: take `&str`, `&[u8]` or a buffer view, return owned data. Do not store references to Python objects past the call; use `Py<T>` when you must keep one.
- `#[pyclass(frozen)]` for immutable shared state; put mutable state behind a `Mutex`. Do not wrap `Rc`, `Arc` or `RefCell` types in the public signature.
- Declare free-threaded support (`#[pymodule(gil_used = false)]`) only after checking that no shared state is unsynchronised, and test on a free-threaded build.

See also [senior-engineering.md](../../architecture/senior-engineering.md) for the shape of a well-confined `unsafe` boundary.

## Unsafe and C libraries

- `unsafe` only for FFI or a measured need. Every block gets `// SAFETY:` stating why the invariants hold; every `unsafe fn` gets a `# Safety` doc section. Keep it in the smallest module and expose a safe API. Run Miri over it.
- Wrapping a C library: a `-sys` crate (generated with `bindgen`) plus a safe crate. `#[repr(C)]` on shared structs, `CString`/`CStr` for strings, free on the side that allocated, an RAII type whose `Drop` releases C-owned memory, check for null.
- No `unsafe impl Send` to silence the compiler; no `transmute` to cast enums or dodge lifetimes.

## The core crate

The crate without PyO3 is ordinary Rust, and its mistakes surface in Python as wrong results. Checked against the Rust API Guidelines and the digests in BeautifulRust (read 10 November 2026):

- One error enum for the crate, implementing `Display` and `std::error::Error` and keeping the cause (`source()`); no `String`, `()` or `Box<dyn Error>` as a public error, and no `map_err(|_| ...)` that drops what failed. The binding crate turns it into a Python exception in one place.
- Put invariants in types: a newtype for each id or unit, an enum instead of a `bool` flag or a "must be X when Y" comment, a constructor that validates once. `#[non_exhaustive]` on a public enum or struct that will grow.
- Conversions that can lose data use `try_from`, not `as`: a wrapped length from Python is a wrong answer, not an error.
- A hand-written `Ord`, `PartialEq` or `Hash` must agree with the others, or maps, sorts and `dedup` corrupt silently. Derive them together unless there is a reason not to.
- `HashMap` iteration order must not reach output, a returned list or a test expectation; sort, or use `BTreeMap` or `IndexMap`.
- Borrowed parameters (`&str`, `&[T]`), no clone made only to satisfy the borrow checker, no lock guard held across `.await` or a call back into Python.
- Public items document `# Errors`, `# Panics` and `# Safety` where they apply; `cargo doc --no-deps` runs clean.

## Types, stubs, tests

- Ship `py.typed` and a hand-written `.pyi` for `<pkg>._core`; check it in CI with `python -m mypy.stubtest <pkg>`.
- Unit tests in the core crate; `pytest` against the installed wheel (`maturin develop` or `uv run --reinstall`) for the binding, including the error paths and the pure-Python reference comparison.

## Style and lints

Idiomatic Rust: `&str` not `&String`, `Option` not sentinels, no `bool` parameters in public signatures, `Debug` on public types, no `get_` prefixes. Configure lints once in `Cargo.toml` (`[lints]` or `[workspace.lints]`); suppress with `#[expect(lint, reason = "...")]` on the narrowest item, never a crate-wide `allow`. Run `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test` before reporting done.
