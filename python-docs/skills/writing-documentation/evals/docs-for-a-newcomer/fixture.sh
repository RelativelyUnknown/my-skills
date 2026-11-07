#!/usr/bin/env bash
# Builds the fixture project for the `docs-for-a-newcomer` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "reconcile"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/reconcile/__init__.py)"
cat > src/reconcile/__init__.py <<'__FIXTURE_EOF__'
from reconcile.core import net, reconcile

__all__ = ["net", "reconcile"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/reconcile/core.py)"
cat > src/reconcile/core.py <<'__FIXTURE_EOF__'
"""Ledger reconciliation."""


def net(entries):
    return sum(e["amount"] for e in entries)


def reconcile(book, bank, lag=2, tol=0.005):
    unmatched = []
    pool = list(bank)
    for b in book:
        for i, c in enumerate(pool):
            if abs(b["amount"] - c["amount"]) <= tol and 0 <= (c["day"] - b["day"]) <= lag:
                del pool[i]
                break
        else:
            unmatched.append(b)
    return unmatched, pool
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_core.py)"
cat > tests/test_core.py <<'__FIXTURE_EOF__'
from reconcile import reconcile


def test_match():
    left, right = reconcile([{"amount": 10.0, "day": 1}], [{"amount": 10.0, "day": 2}])
    assert left == [] and right == []
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
