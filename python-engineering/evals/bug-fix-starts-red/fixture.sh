#!/usr/bin/env bash
# Builds the fixture project for the `bug-fix-starts-red` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pricing"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/pricing/__init__.py)"
cat > src/pricing/__init__.py <<'__FIXTURE_EOF__'
from pricing.discount import apply_discount

__all__ = ["apply_discount"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/pricing/discount.py)"
cat > src/pricing/discount.py <<'__FIXTURE_EOF__'
def apply_discount(price: float, percent: float) -> float:
    """Return price reduced by percent, rounded to cents (half up)."""
    return price * (1 - percent / 100)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_discount.py)"
cat > tests/test_discount.py <<'__FIXTURE_EOF__'
import pytest

from pricing import apply_discount


def test_zero_percent_returns_price():
    assert apply_discount(10.0, 0) == 10.0


def test_full_discount_is_free():
    assert apply_discount(10.0, 100) == 0.0


@pytest.mark.parametrize(("price", "percent", "expected"), [(100.0, 50, 50.0), (80.0, 25, 60.0)])
def test_whole_cent_results(price, percent, expected):
    assert apply_discount(price, percent) == expected
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
