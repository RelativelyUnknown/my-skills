#!/usr/bin/env bash
# Builds the fixture project for the `audit-repo-bloat-and-load` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "shopstats"
version = "0.9.0"
requires-python = ">=3.12"

[project.scripts]
shopstats = "shopstats.cli:main"
shopstats-export = "shopstats.cli:export_cmd"

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# shopstats

Back-office tools: customer totals, coupons, refunds and an export.
Used by about thirty staff through `shopstats` and `shopstats-export`.
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/__init__.py)"
cat > src/shopstats/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/db.py)"
cat > src/shopstats/db.py <<'__FIXTURE_EOF__'
import sqlite3


def connect(path: str = "shop.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/orders.py)"
cat > src/shopstats/orders.py <<'__FIXTURE_EOF__'
import sqlite3


def totals_by_customer(conn: sqlite3.Connection) -> dict[str, float]:
    """Return the sum of order totals for every customer."""
    totals: dict[str, float] = {}
    for customer in conn.execute("SELECT id, name FROM customers"):
        row = conn.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE customer_id = ?", (customer["id"],)).fetchone()
        totals[customer["name"]] = row[0]
    return totals
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/coupons.py)"
cat > src/shopstats/coupons.py <<'__FIXTURE_EOF__'
import sqlite3


def claim_coupon(conn: sqlite3.Connection, code: str, user_id: int) -> bool:
    """Give the coupon to the user if it is still unused."""
    row = conn.execute("SELECT used FROM coupons WHERE code = ?", (code,)).fetchone()
    if row is None or row["used"]:
        return False
    conn.execute("UPDATE coupons SET used = 1, user_id = ? WHERE code = ?", (user_id, code))
    conn.commit()
    return True
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/refunds.py)"
cat > src/shopstats/refunds.py <<'__FIXTURE_EOF__'
def apply_refund(order_total: float, refund: float, fee_pct: float) -> float:
    """Return what the customer gets back after the processing fee."""
    if refund > order_total:
        refund = order_total
    fee = refund * fee_pct / 100
    return round(refund - fee, 2)
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/search.py)"
cat > src/shopstats/search.py <<'__FIXTURE_EOF__'
def find_product(products: list[dict[str, str]], name: str) -> dict[str, str] | None:
    # shortcut: linear scan over ~200 products, move to a dict index past 10k products
    for product in products:
        if product["name"] == name:
            return product
    return None
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/legacy.py)"
cat > src/shopstats/legacy.py <<'__FIXTURE_EOF__'
def format_invoice_v1(number: int, total: float) -> str:
    return f"INV{number:06d} {total:.2f}"
__FIXTURE_EOF__
mkdir -p "$(dirname src/shopstats/cli.py)"
cat > src/shopstats/cli.py <<'__FIXTURE_EOF__'
import sys

from shopstats import db, orders


def main() -> int:
    conn = db.connect()
    for name, total in sorted(orders.totals_by_customer(conn).items()):
        print(f"{name}\t{total:.2f}")
    return 0


def export_cmd() -> int:
    """Console script `shopstats-export`: write all customer totals as CSV on stdout."""
    conn = db.connect()
    for name, total in orders.totals_by_customer(conn).items():
        sys.stdout.write(f"{name},{total}\n")
    return 0
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_orders.py)"
cat > tests/test_orders.py <<'__FIXTURE_EOF__'
import sqlite3

from shopstats.orders import totals_by_customer


def test_totals():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript("CREATE TABLE customers (id INTEGER, name TEXT); CREATE TABLE orders (customer_id INTEGER, total REAL);"
                       "INSERT INTO customers VALUES (1, 'ann'); INSERT INTO orders VALUES (1, 5.0), (1, 2.5);")
    assert totals_by_customer(conn) == {"ann": 7.5}
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
