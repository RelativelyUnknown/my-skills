#!/usr/bin/env bash
# Builds the fixture project for the `optional-parquet-dependency` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "reports"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/reports/__init__.py)"
cat > src/reports/__init__.py <<'__FIXTURE_EOF__'
from reports.rows import summarize

__all__ = ["summarize"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/reports/rows.py)"
cat > src/reports/rows.py <<'__FIXTURE_EOF__'
from collections.abc import Iterable, Mapping


def summarize(rows: Iterable[Mapping[str, int]]) -> dict[str, int]:
    """Return per-key totals across rows."""
    totals: dict[str, int] = {}
    for row in rows:
        for key, value in row.items():
            totals[key] = totals.get(key, 0) + value
    return totals
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_rows.py)"
cat > tests/test_rows.py <<'__FIXTURE_EOF__'
from reports import summarize


def test_summarize():
    assert summarize([{'a': 1}, {'a': 2}]) == {'a': 3}
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
