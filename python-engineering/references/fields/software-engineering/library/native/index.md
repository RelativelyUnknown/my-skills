# Native extensions: Python with Rust or C

A library whose hot or low-level part is written in Rust or C and called from Python. Read `../shared/index.md` too: everything for a pure-Python library still applies.

- architecture.md: whether to go native, which layer, the layout, the seam, how the two sides are tested.
- rust.md: PyO3 and maturin: errors, the GIL, ownership, stubs, lints, `unsafe`.
- c.md: the CPython C API: reference counts, errors, init, threads, the stable ABI, sanitizers.
- ci-wheels.md: build backends, wheels, CI jobs, release checks.

Formatters and linters (the project's own config wins):

- Python: `ruff check` and `ruff format`, a type checker.
- Rust: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`; lints configured in `Cargo.toml` `[lints]`, never `#![deny(warnings)]` in source.
- C and C++: `clang-format` with the project's `.clang-format`, `-Wall -Wextra -Werror` in CI, `clang-tidy` if configured.

Reviewing a native change: `python-review` has a boundary checklist (`references/native-boundary.md`).
