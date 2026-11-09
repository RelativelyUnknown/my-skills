#!/usr/bin/env bash
# Builds the fixture for the `de-rerunnable-load` case.
set -euo pipefail
mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "orders-etl"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
__FIXTURE_EOF__
mkdir -p "$(dirname load_orders.py)"
cat > load_orders.py <<'__FIXTURE_EOF__'
"""Nightly load of yesterday's orders from the export file into the warehouse table."""
import csv
import sqlite3
from datetime import date, timedelta


def main() -> None:
    day = date.today() - timedelta(days=1)
    conn = sqlite3.connect("warehouse.db")
    conn.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT, day TEXT, total REAL)")
    with open(f"exports/orders-{day}.csv", newline="") as f:
        for row in csv.DictReader(f):
            conn.execute("INSERT INTO orders VALUES (?, ?, ?)", (row["order_id"], str(day), float(row["total"])))
    conn.commit()


if __name__ == "__main__":
    main()
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
