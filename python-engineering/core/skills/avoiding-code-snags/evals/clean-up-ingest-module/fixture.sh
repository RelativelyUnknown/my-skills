#!/usr/bin/env bash
# Builds the fixture project for the `clean-up-ingest-module` case in the empty workspace.
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

__FIXTURE_EOF__
mkdir -p "$(dirname src/reports/ingest.py)"
cat > src/reports/ingest.py <<'__FIXTURE_EOF__'
"""Ingest module.

This module ingests reports. It has functions that load reports and a class that runs them.
"""
import json
import logging
from datetime import datetime
from os.path import *
from typing import Any

logger = logging.getLogger(__name__)

_CACHE = {}


def _split_fields(line):
    """Return (name, amount) from a 'name,amount' line; the amount may use '_' as a thousands separator."""
    name, _, raw = line.partition(",")
    return name.strip(), raw.strip().replace("_", "")


def parse_amount(raw, default=0):
    # Step 1: try to convert the amount
    try:
        return float(raw)
    except Exception:
        pass
    return default


def load_report(path, rows=[]):
    """Return the rows of the report at path, or None when the file does not exist."""
    if path in _CACHE:
        return _CACHE[path]
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return None
    for line in lines:
        name, raw = _split_fields(line)
        rows.append({"name": name, "amount": parse_amount(raw)})
    # rows.sort(key=lambda r: r["name"])
    # print(rows)
    print("DEBUG: loaded", len(rows))
    _CACHE[path] = rows
    return rows


def get_data(d: dict[str, Any]) -> dict[str, Any]:
    assert isinstance(d, dict)
    out = {}
    out["timestamp"] = datetime.utcnow().isoformat()
    out["total"] = sum(r["amount"] for r in d["rows"])
    return out


def summarize(rows, timeout=None):
    timeout = timeout or 30
    if len(rows) == 0:
        return {"count": 0, "timeout": timeout}
    return {"count": len(rows), "timeout": timeout}


def top(rows, n):
    return sorted(rows, key=lambda r: r["amount"], reverse=True)[:n]  # type: ignore[arg-type]  # stub types amount as str; it is a float at runtime


class ReportManager:
    def __init__(self):
        pass

    def run(self, path, flag, verbose):
        report = load_report(path)
        if report == None:
            return None
        if flag == True:
            report = [r for r in report if r["amount"] > 0]
        try:
            data = get_data({"rows": report})
        except Exception as e:
            logger.error("failed: %s", e)
            raise
        if verbose:
            print(data)
        return data
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_ingest.py)"
cat > tests/test_ingest.py <<'__FIXTURE_EOF__'
from reports.ingest import get_data, load_report, parse_amount, summarize, top


def test_parse_amount_reads_numbers():
    assert parse_amount("12.5") == 12.5


def test_parse_amount_defaults_on_garbage():
    assert parse_amount("n/a") == 0


def test_load_report_missing_file_returns_none(tmp_path):
    assert load_report(tmp_path / "nope.csv") is None


def test_load_report_parses_rows(tmp_path):
    path = tmp_path / "r.csv"
    path.write_text("a,1\nb,2_000\n")
    assert load_report(str(path)) == [
        {"name": "a", "amount": 1.0},
        {"name": "b", "amount": 2000.0},
    ]


def test_get_data_totals_amounts():
    assert get_data({"rows": [{"amount": 1}, {"amount": 2}]})["total"] == 3


def test_summarize_counts_rows_and_keeps_timeout():
    assert summarize([]) == {"count": 0, "timeout": 30}
    assert summarize([1, 2], timeout=5) == {"count": 2, "timeout": 5}


def test_top_returns_largest_first():
    assert top([{"amount": 1.0}, {"amount": 3.0}], 1) == [{"amount": 3.0}]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
