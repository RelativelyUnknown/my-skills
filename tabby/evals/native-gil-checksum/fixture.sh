#!/usr/bin/env bash
# Builds the fixture for the `native-gil-checksum` case: a small maturin project on PyO3 0.30.
set -euo pipefail
mkdir -p src python/fastcsv tests
cat > Cargo.toml <<'__FIXTURE_EOF__'
[package]
name = "fastcsv"
version = "0.1.0"
edition = "2021"

[lib]
name = "_core"
crate-type = ["cdylib"]

[dependencies]
pyo3 = "0.30"
__FIXTURE_EOF__
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["maturin>=1.9,<2"]
build-backend = "maturin"

[project]
name = "fastcsv"
version = "0.1.0"
requires-python = ">=3.12"

[tool.maturin]
python-source = "python"
module-name = "fastcsv._core"
__FIXTURE_EOF__
cat > src/lib.rs <<'__FIXTURE_EOF__'
use pyo3::prelude::*;

/// Count the commas in a line.
#[pyfunction]
fn count_commas(line: &str) -> usize {
    line.matches(',').count()
}

#[pymodule]
mod _core {
    #[pymodule_export]
    use super::count_commas;
}
__FIXTURE_EOF__
cat > python/fastcsv/__init__.py <<'__FIXTURE_EOF__'
from fastcsv._core import count_commas

__all__ = ["count_commas"]
__FIXTURE_EOF__
cat > python/fastcsv/_core.pyi <<'__FIXTURE_EOF__'
def count_commas(line: str) -> int: ...
__FIXTURE_EOF__
touch python/fastcsv/py.typed
cat > tests/test_count.py <<'__FIXTURE_EOF__'
from fastcsv import count_commas


def test_count_commas():
    assert count_commas("a,b,c") == 2
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
