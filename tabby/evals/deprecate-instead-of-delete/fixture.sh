#!/usr/bin/env bash
# Builds the fixture project for the `deprecate-instead-of-delete` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "tinydates"
version = "1.4.0"
requires-python = ">=3.12"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# tinydates

Small helpers for timestamps. `parse_ts("2026-11-03T10:00:00")` returns a `datetime`.
__FIXTURE_EOF__
mkdir -p "$(dirname CHANGELOG.md)"
cat > CHANGELOG.md <<'__FIXTURE_EOF__'
# Changelog

## [1.4.0] - 2026-10-20
### Added
- `fmt_ts` formats a datetime the way `parse_ts` reads it.
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinydates/__init__.py)"
cat > src/tinydates/__init__.py <<'__FIXTURE_EOF__'
from tinydates.compat import fmt_ts, parse_ts

__all__ = ["fmt_ts", "parse_ts"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinydates/compat.py)"
cat > src/tinydates/compat.py <<'__FIXTURE_EOF__'
from datetime import datetime


def parse_ts(value: str) -> datetime:
    """Parse an ISO 8601 timestamp such as 2026-11-03T10:00:00."""
    date, _, clock = value.partition("T")
    year, month, day = (int(part) for part in date.split("-"))
    hour, minute, second = (int(part) for part in clock.split(":"))
    return datetime(year, month, day, hour, minute, second)


def fmt_ts(value: datetime) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%S")
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinydates/reports.py)"
cat > src/tinydates/reports.py <<'__FIXTURE_EOF__'
from tinydates.compat import parse_ts


def age_days(created: str, now: str) -> int:
    return (parse_ts(now) - parse_ts(created)).days
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinydates/sync.py)"
cat > src/tinydates/sync.py <<'__FIXTURE_EOF__'
from tinydates.compat import parse_ts


def is_newer(a: str, b: str) -> bool:
    return parse_ts(a) > parse_ts(b)
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinydates/cli.py)"
cat > src/tinydates/cli.py <<'__FIXTURE_EOF__'
import sys

from tinydates.compat import parse_ts


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    print(parse_ts(args[0]).isoformat())
    return 0
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_compat.py)"
cat > tests/test_compat.py <<'__FIXTURE_EOF__'
from datetime import datetime

from tinydates import parse_ts


def test_parse_ts():
    assert parse_ts("2026-11-03T10:00:00") == datetime(2026, 11, 3, 10, 0, 0)
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
