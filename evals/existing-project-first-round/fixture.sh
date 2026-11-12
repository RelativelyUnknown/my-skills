#!/usr/bin/env bash
# Builds a small Rust-backed Python library in the empty workspace.
set -euo pipefail
mkdir -p python/fastsum src .github/workflows tests docs
cat > pyproject.toml <<'__F__'
[build-system]
requires = ["maturin>=1.9,<2"]
build-backend = "maturin"

[project]
name = "fastsum"
version = "0.2.0"
requires-python = ">=3.10"
description = "Fast checksums for Python, with a Rust core"

[tool.maturin]
python-source = "python"
module-name = "fastsum._core"

[dependency-groups]
dev = ["pytest", "ruff", "mypy"]
__F__
cat > Cargo.toml <<'__F__'
[package]
name = "fastsum"
version = "0.2.0"
edition = "2021"

[lib]
name = "_core"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.26", features = ["abi3-py310"] }
__F__
cat > src/lib.rs <<'__F__'
use pyo3::prelude::*;

#[pyfunction]
fn crc(data: &[u8]) -> u32 {
    data.iter().fold(0u32, |a, b| a.rotate_left(5) ^ u32::from(*b))
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crc, m)?)
}
__F__
cat > python/fastsum/__init__.py <<'__F__'
from fastsum._core import crc

__all__ = ["crc"]
__F__
touch python/fastsum/py.typed
cat > tests/test_crc.py <<'__F__'
from fastsum import crc


def test_empty():
    assert crc(b"") == 0
__F__
cat > Makefile <<'__F__'
check:
	ruff check . && ruff format --check . && cargo clippy -- -D warnings && maturin develop && pytest
__F__
cat > .github/workflows/ci.yml <<'__F__'
name: ci
on: [push]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make check
__F__
cat > README.md <<'__F__'
# fastsum

Fast checksums for Python.
__F__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
