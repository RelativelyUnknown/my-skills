#!/usr/bin/env bash
# Builds the fixture project in the empty workspace. Run by `claude plugin eval --scaffold`.
set -euo pipefail

mkdir -p src/orders tests
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "orders"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
: > src/orders/__init__.py
cat > src/orders/totals.py <<'__FIXTURE_EOF__'
def line_total_cents(price_cents: int, quantity: int) -> int:
    return price_cents * quantity
__FIXTURE_EOF__
cat > tests/test_totals.py <<'__FIXTURE_EOF__'
from orders.totals import line_total_cents


def test_line_total_cents():
    assert line_total_cents(250, 3) == 750
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
