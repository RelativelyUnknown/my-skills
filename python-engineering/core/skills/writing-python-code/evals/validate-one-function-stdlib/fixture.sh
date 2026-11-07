#!/usr/bin/env bash
# Builds the fixture project for the `validate-one-function-stdlib` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/__init__.py)"
cat > src/shop/__init__.py <<'__FIXTURE_EOF__'
from shop.pricing import apply_coupon

__all__ = ["apply_coupon"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/pricing.py)"
cat > src/shop/pricing.py <<'__FIXTURE_EOF__'
def apply_coupon(price, percent):
    """Return the price after a percentage coupon."""
    return round(price * (1 - percent / 100), 2)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_pricing.py)"
cat > tests/test_pricing.py <<'__FIXTURE_EOF__'
from shop import apply_coupon


def test_half_price():
    assert apply_coupon(10.0, 50) == 5.0
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
