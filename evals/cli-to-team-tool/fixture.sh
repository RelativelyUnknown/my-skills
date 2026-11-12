#!/usr/bin/env bash
# Builds the fixture project for the `cli-to-team-tool` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "csvstat"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# csvstat

Totals and averages for the sales CSV.
__FIXTURE_EOF__
mkdir -p "$(dirname src/csvstat/__init__.py)"
cat > src/csvstat/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/csvstat/main.py)"
cat > src/csvstat/main.py <<'__FIXTURE_EOF__'
import csv

DATA = "/home/dev/data/sales.csv"


def main():
    rows = list(csv.DictReader(open(DATA)))
    amounts = [float(r["amount"]) for r in rows]
    print(f"rows: {len(rows)}")
    print(f"total: {sum(amounts):.2f}")
    print(f"average: {sum(amounts) / len(amounts):.2f}")


if __name__ == "__main__":
    main()
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_main.py)"
cat > tests/test_main.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
