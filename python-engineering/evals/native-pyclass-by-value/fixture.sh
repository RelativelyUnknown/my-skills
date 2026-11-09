#!/usr/bin/env bash
# Builds the fixture for the `native-pyclass-by-value` case: a small maturin project on PyO3 0.30.
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

/// A point in the plane.
#[pyclass]
#[derive(Clone)]
struct Point {
    #[pyo3(get)]
    x: f64,
    #[pyo3(get)]
    y: f64,
}

#[pymethods]
impl Point {
    #[new]
    fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }
}

#[pymodule]
mod _core {
    #[pymodule_export]
    use super::Point;
}
__FIXTURE_EOF__
cat > python/fastcsv/__init__.py <<'__FIXTURE_EOF__'
from fastcsv._core import Point

__all__ = ["Point"]
__FIXTURE_EOF__
cat > python/fastcsv/_core.pyi <<'__FIXTURE_EOF__'
class Point:
    x: float
    y: float
    def __init__(self, x: float, y: float) -> None: ...
__FIXTURE_EOF__
touch python/fastcsv/py.typed
cat > tests/test_count.py <<'__FIXTURE_EOF__'
from fastcsv import Point


def test_point():
    assert Point(1.0, 2.0).x == 1.0
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
