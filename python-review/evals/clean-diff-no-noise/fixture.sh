#!/usr/bin/env bash
# Builds the fixture project for the `clean-diff-no-noise` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "orders"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27"]

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'
from orders.store import list_orders

__all__ = ["list_orders"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/store.py)"
cat > src/orders/store.py <<'__FIXTURE_EOF__'
_ORDERS = [{"id": 1, "total": 10}, {"id": 2, "total": 25}]


def list_orders() -> list[dict]:
    """Return all orders."""
    return list(_ORDERS)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_store.py)"
cat > tests/test_store.py <<'__FIXTURE_EOF__'
from orders import list_orders


def test_list_orders_returns_all():
    assert [o["id"] for o in list_orders()] == [1, 2]


def test_list_orders_returns_copy():
    list_orders().clear()
    assert len(list_orders()) == 2
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base

git checkout -q -b feature
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'
from orders.store import list_orders, total_revenue

__all__ = ["list_orders", "total_revenue"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/store.py)"
cat > src/orders/store.py <<'__FIXTURE_EOF__'
_ORDERS = [{"id": 1, "total": 10}, {"id": 2, "total": 25}]


def list_orders() -> list[dict]:
    """Return all orders."""
    return list(_ORDERS)


def total_revenue() -> int:
    """Return the sum of all order totals."""
    return sum(order["total"] for order in _ORDERS)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_revenue.py)"
cat > tests/test_revenue.py <<'__FIXTURE_EOF__'
from orders import total_revenue


def test_total_revenue_sums_order_totals():
    assert total_revenue() == 35
__FIXTURE_EOF__
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm feature
git checkout -q main
