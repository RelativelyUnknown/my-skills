#!/usr/bin/env bash
# Builds the fixture project for the `do-not-over-engineer-orders` case in the empty workspace.
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
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/core.py)"
cat > src/orders/core.py <<'__FIXTURE_EOF__'
import json
import sqlite3
from datetime import datetime
from urllib.request import Request, urlopen


def process_order(order_id, items, db_path="orders.db"):
    subtotal = sum(i["price"] * i["qty"] for i in items)
    discount = subtotal * 0.1 if datetime.now().weekday() == 4 else 0
    tax = round((subtotal - discount) * 0.2, 2)
    total = round(subtotal - discount + tax, 2)
    req = Request(
        "https://api.example.com/charge",
        data=json.dumps({"id": order_id, "amount": total}).encode(),
        method="POST",
    )
    with urlopen(req) as resp:
        ok = json.load(resp)["ok"]
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT, total REAL, paid INTEGER)")
    conn.execute("INSERT INTO orders VALUES (?, ?, ?)", (order_id, total, int(ok)))
    conn.commit()
    conn.close()
    return total if ok else None
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_core.py)"
cat > tests/test_core.py <<'__FIXTURE_EOF__'
import io
import json
from unittest import mock

from orders import core


def test_process_order_charges_and_stores(tmp_path):
    fake = mock.MagicMock()
    fake.__enter__.return_value = io.StringIO(json.dumps({"ok": True}))
    with mock.patch.object(core, "urlopen", return_value=fake), mock.patch.object(core, "datetime") as dt:
        dt.now.return_value.weekday.return_value = 0
        total = core.process_order("o1", [{"price": 10.0, "qty": 2}], db_path=str(tmp_path / "o.db"))
    assert total == 24.0
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
