#!/usr/bin/env bash
# Builds the fixture project for the `port-hot-path-to-rust` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname Cargo.toml)"
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
mkdir -p "$(dirname pyproject.toml)"
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
mkdir -p "$(dirname src/lib.rs)"
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
mkdir -p "$(dirname python/fastcsv/__init__.py)"
cat > python/fastcsv/__init__.py <<'__FIXTURE_EOF__'
from fastcsv._core import count_commas
from fastcsv.ranking import rank_items

__all__ = ["count_commas", "rank_items"]
__FIXTURE_EOF__
mkdir -p "$(dirname python/fastcsv/_core.pyi)"
cat > python/fastcsv/_core.pyi <<'__FIXTURE_EOF__'
def count_commas(line: str) -> int: ...
__FIXTURE_EOF__
mkdir -p "$(dirname python/fastcsv/py.typed)"
cat > python/fastcsv/py.typed <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname python/fastcsv/ranking.py)"
cat > python/fastcsv/ranking.py <<'__FIXTURE_EOF__'
def rank_items(items: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Return (name, score) pairs, best first.

    Scores are rounded to one decimal (Python's round: halves go to the even
    digit) before sorting, so items that tie after rounding keep input order.
    """
    return sorted(((name, round(score, 1)) for name, score in items), key=lambda pair: -pair[1])
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_rank.py)"
cat > tests/test_rank.py <<'__FIXTURE_EOF__'
from fastcsv import rank_items


def test_best_first():
    assert rank_items([("a", 1.0), ("b", 3.0)]) == [("b", 3.0), ("a", 1.0)]


def test_ties_keep_input_order():
    assert rank_items([("x", 2.0), ("y", 2.0), ("z", 2.0)]) == [("x", 2.0), ("y", 2.0), ("z", 2.0)]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
