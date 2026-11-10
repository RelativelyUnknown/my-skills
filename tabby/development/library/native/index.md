# Native extensions: Python with Rust, C or C++

A library whose hot or low-level part is written in Rust, C, C++ or (rarely) Zig and called from Python. Read `../shared/index.md` too: everything for a pure-Python library still applies.

- architecture.md: whether to go native, which layer, the layout, the seam, how the two sides are tested.
- rust.md: PyO3 and maturin: errors, the GIL, ownership, stubs, lints, `unsafe`.
- c.md: the CPython C API: reference counts, errors, init, threads, the stable ABI, sanitizers.
- cpp.md: C++ with nanobind or pybind11: ownership and return policies, exceptions, the GIL, stubs, the stable ABI.
- zig.md: Ziggy Pydust, when the project already uses Zig or wants its comptime model; prefer Rust for new native code.
- smells.md: native boundary mistakes in Rust, PyO3, the C API and C++ bindings. Read before finishing a native change.
- ci-wheels.md: build backends, wheels, CI jobs, release checks.

Formatters and linters (the project's own config wins):

- Python: `ruff check` and `ruff format`, a type checker.
- Rust: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`; lints configured in `Cargo.toml` `[lints]`, never `#![deny(warnings)]` in source.
- C and C++: `clang-format` with the project's `.clang-format`, `-Wall -Wextra -Werror` in CI, `clang-tidy` if configured.
- Zig: `zig fmt --check`, `zig build test`.

Reviewing a native change: the `review` module has a boundary checklist (`review/native-boundary.md`).
