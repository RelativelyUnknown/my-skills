#!/usr/bin/env bash
# Builds the fixture project for the `scout-reports-what-it-noticed` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "orders"
version = "0.3.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/summary.py)"
cat > src/orders/summary.py <<'__FIXTURE_EOF__'
from collections import defaultdict


def top_customers(orders: list[tuple[str, float]], n: int = 3) -> list[tuple[str, float]]:
    """Return the n customers with the largest total, best first. `orders` is (customer, amount) pairs."""
    totals: dict[str, float] = defaultdict(float)
    for customer, amount in orders:
        totals[customer] += amount
    return sorted(totals.items(), key=lambda pair: pair[1], reverse=True)[:n]


def dedupe_ids(ids: list[int]) -> list[int]:
    """Return ids without repeats, keeping first-seen order."""
    result: list[int] = []
    for i in ids:
        if i not in result:
            result.append(i)
    return result


def chunk(seq: list[int], size: int) -> list[list[int]]:
    out = []
    for start in range(0, len(seq), size):
        out.append(seq[start:start + size])
    return out
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_summary.py)"
cat > tests/test_summary.py <<'__FIXTURE_EOF__'
from orders.summary import top_customers


def test_top_customers():
    assert top_customers([("a", 1.0), ("b", 5.0), ("a", 2.0)], n=2) == [("b", 5.0), ("a", 3.0)]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
