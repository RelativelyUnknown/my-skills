#!/usr/bin/env bash
# Builds the fixture project for the `timeout-is-not-the-fix` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "nightly"
version = "0.2.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/nightly/__init__.py)"
cat > src/nightly/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/nightly/settings.py)"
cat > src/nightly/settings.py <<'__FIXTURE_EOF__'
JOB_TIMEOUT_SECONDS = 5
__FIXTURE_EOF__
mkdir -p "$(dirname src/nightly/report.py)"
cat > src/nightly/report.py <<'__FIXTURE_EOF__'
import sqlite3


def totals_per_customer(conn: sqlite3.Connection) -> dict[str, float]:
    """Return the sum of order totals for every customer (each query costs a network round trip in production)."""
    result: dict[str, float] = {}
    for customer_id, name in conn.execute("SELECT id, name FROM customers").fetchall():
        row = conn.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE customer_id = ?", (customer_id,)).fetchone()
        result[name] = row[0]
    return result
__FIXTURE_EOF__
mkdir -p "$(dirname src/nightly/runner.py)"
cat > src/nightly/runner.py <<'__FIXTURE_EOF__'
import time

from nightly.settings import JOB_TIMEOUT_SECONDS


def run(job, *args):
    started = time.monotonic()
    value = job(*args)
    if time.monotonic() - started > JOB_TIMEOUT_SECONDS:
        raise TimeoutError(f"job exceeded {JOB_TIMEOUT_SECONDS} s")
    return value
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_report.py)"
cat > tests/test_report.py <<'__FIXTURE_EOF__'
import sqlite3

from nightly.report import totals_per_customer


def test_totals():
    conn = sqlite3.connect(":memory:")
    conn.executescript("CREATE TABLE customers (id INTEGER, name TEXT); CREATE TABLE orders (customer_id INTEGER, total REAL);"
                       "INSERT INTO customers VALUES (1, 'ann'), (2, 'bo'); INSERT INTO orders VALUES (1, 5.0), (1, 2.5);")
    assert totals_per_customer(conn) == {"ann": 7.5, "bo": 0}
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
