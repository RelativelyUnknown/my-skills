# Wheels, builds, CI for native extensions

## Build backend

| Native code | Backend |
| --- | --- |
| Rust and PyO3 | `maturin` |
| C or C++ with CMake | `scikit-build-core` |
| Meson projects (numpy, pandas style) | `meson-python` |
| Small C extension | `setuptools` (`ext_modules`) |

Commit `Cargo.lock` and the toolchain files (`rust-toolchain.toml`, `.clang-format`, `rustfmt.toml`, `clippy.toml`). Make sure the sdist includes every file the build needs (maturin `include = [...]` for `rust-toolchain.toml`, licences and generated sources) and build from it once in CI.

## Wheels

- Build wheels with `cibuildwheel` (or `maturin-action` for Rust): Linux (manylinux and musllinux), macOS (x86_64, arm64), Windows.
- One `abi3` wheel per platform when the stable ABI is enough (limited API, `abi3-pyXY` for PyO3); otherwise one wheel per interpreter version. Add free-threaded builds (`cp314t`) only when the module declares support.
- Test the installed wheel, not the source tree: `test-command = "pytest {project}/tests"` in `cibuildwheel`.

## CI jobs (separate, so a failure names its cause)

1. **Lint:** `ruff check`, `ruff format --check`, type check; `cargo fmt --check`, `cargo clippy -- -D warnings`; `clang-format --dry-run` for C.
2. **Tests:** Linux, macOS, Windows; oldest and newest supported Python; `cargo test` for the core crate.
3. **Stubs:** `python -m mypy.stubtest <pkg>`.
4. **Sanitizers (C):** ASan and UBSan build, full suite. Rust `unsafe`: Miri on the core crate.
5. **Free-threaded:** a `python3.14t` job, only if the module claims support.
6. **Benchmarks:** a tracked benchmark so a regression of the native path is visible.
7. **Wheels and sdist:** build, install into a clean environment, import, run the smoke test.

One canonical check command (for example `nox -e local`, `make check` or a `uv run` task) runs the lint, test and stub steps locally; record it in `commands:` of the `## Tabby` section.

## Release checks

- Version in one place ([versioning.md](../shared/versioning.md)); the native crate version follows it or is documented as separate.
- The wheel imports on a machine with no compiler; the fallback path still works when the native module is absent.
- `pip install` from the sdist works with a compiler; the error message when the toolchain is missing says what to install.
- Publish with trusted publishing; do not store tokens ([release.md](../shared/release.md)).
