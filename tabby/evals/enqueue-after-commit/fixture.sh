#!/usr/bin/env bash
# Builds the fixture project for the `enqueue-after-commit` case in the empty workspace.
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

__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/orders.py)"
cat > src/shop/orders.py <<'__FIXTURE_EOF__'
import sqlite3

QUEUE: list[int] = []


def enqueue_receipt(order_id: int) -> None:
    """Stand-in for `send_receipt.delay(order_id)`: a worker may run it at once."""
    QUEUE.append(order_id)


def create_order(conn: sqlite3.Connection, customer: str) -> int:
    conn.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer TEXT NOT NULL)")
    cur = conn.execute("INSERT INTO orders (customer) VALUES (?)", (customer,))
    return int(cur.lastrowid)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
