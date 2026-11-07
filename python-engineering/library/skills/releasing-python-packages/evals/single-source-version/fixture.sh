#!/usr/bin/env bash
# Builds the fixture project for the `single-source-version` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname CHANGELOG.md)"
cat > CHANGELOG.md <<'__FIXTURE_EOF__'
# Changelog

## 0.3.0

- Added `double`.
__FIXTURE_EOF__
mkdir -p "$(dirname Makefile)"
cat > Makefile <<'__FIXTURE_EOF__'
check:
	uv run ruff check .
	uv run mypy src
	uv run pytest
__FIXTURE_EOF__
mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "minilib"
version = "0.3.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/minilib/__init__.py)"
cat > src/minilib/__init__.py <<'__FIXTURE_EOF__'
__version__ = "0.3.0"


def double(x: int) -> int:
    return x * 2
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_double.py)"
cat > tests/test_double.py <<'__FIXTURE_EOF__'
from minilib import double


def test_double():
    assert double(2) == 4
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
