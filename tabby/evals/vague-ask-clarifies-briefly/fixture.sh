#!/usr/bin/env bash
# Builds the fixture project for the `vague-ask-clarifies-briefly` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "reportkit"
version = "1.8.2"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
reportkit = "reportkit.cli:main"

[dependency-groups]
dev = ["pytest>=9", "ruff>=0.6"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname Makefile)"
cat > Makefile <<'__FIXTURE_EOF__'
.PHONY: check test lint deploy
check: lint test
lint:
	uv run ruff check .
test:
	uv run pytest
deploy:
	echo deployed > deployed.txt
__FIXTURE_EOF__
mkdir -p "$(dirname .github/workflows/ci.yml)"
cat > .github/workflows/ci.yml <<'__FIXTURE_EOF__'
name: ci
on: [pull_request, push]
permissions:
  contents: read
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7.0.1
      - uses: astral-sh/setup-uv@v10.3.3
      - run: uv sync --locked
      - run: make check
__FIXTURE_EOF__
mkdir -p "$(dirname CHANGELOG.md)"
cat > CHANGELOG.md <<'__FIXTURE_EOF__'
# Changelog

## [1.8.2] - 2026-10-02
### Fixed
- Totals no longer drop the last row of a group.
__FIXTURE_EOF__
mkdir -p "$(dirname src/reportkit/__init__.py)"
cat > src/reportkit/__init__.py <<'__FIXTURE_EOF__'
__all__ = ["render_table"]

from reportkit.report import render_table
__FIXTURE_EOF__
mkdir -p "$(dirname src/reportkit/report.py)"
cat > src/reportkit/report.py <<'__FIXTURE_EOF__'
from collections.abc import Sequence


def render_table(rows: Sequence[tuple[str, float]]) -> str:
    """Return the report as a fixed-width table with a total line."""
    width = max((len(name) for name, _ in rows), default=4)
    lines = [f"{name:<{width}}  {amount:>10.2f}" for name, amount in rows]
    lines.append(f"{'total':<{width}}  {sum(a for _, a in rows):>10.2f}")
    return "\n".join(lines)
__FIXTURE_EOF__
mkdir -p "$(dirname src/reportkit/client.py)"
cat > src/reportkit/client.py <<'__FIXTURE_EOF__'
import json
import urllib.request


def fetch_rows(url: str) -> list[tuple[str, float]]:
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.load(response)
    return [(item["name"], float(item["amount"])) for item in data]
__FIXTURE_EOF__
mkdir -p "$(dirname src/reportkit/cli.py)"
cat > src/reportkit/cli.py <<'__FIXTURE_EOF__'
"""Print the sales report."""
import argparse
import sys

from reportkit.client import fetch_rows
from reportkit.report import render_table


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args(argv)
    try:
        rows = fetch_rows(args.url)
    except OSError as error:
        print(f"cannot fetch {args.url}: {error}", file=sys.stderr)
        return 1
    print(render_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_report.py)"
cat > tests/test_report.py <<'__FIXTURE_EOF__'
from reportkit.report import render_table


def test_total_line():
    assert render_table([("a", 1.0), ("b", 2.5)]).splitlines()[-1].endswith("3.50")
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# reportkit

Prints the weekly sales report for the finance team.

    reportkit https://sales.example.com/api/week
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
echo "- change 0" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 0"
echo "- change 1" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 1"
echo "- change 2" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 2"
echo "- change 3" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 3"
echo "- change 4" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 4"
echo "- change 5" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 5"
echo "- change 6" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 6"
echo "- change 7" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 7"
echo "- change 8" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 8"
echo "- change 9" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 9"
echo "- change 10" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 10"
echo "- change 11" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 11"
echo "- change 12" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 12"
echo "- change 13" >> CHANGELOG.md; git add -A; git -c user.email=eval@example.com -c user.name=eval commit -qm "change 13"
