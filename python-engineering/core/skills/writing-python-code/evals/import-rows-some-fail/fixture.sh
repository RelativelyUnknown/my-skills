#!/usr/bin/env bash
# Builds the fixture project for the `import-rows-some-fail` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "ledger"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/ledger/__init__.py)"
cat > src/ledger/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/ledger/store.py)"
cat > src/ledger/store.py <<'__FIXTURE_EOF__'
def import_one(row: dict) -> None:
    """Stand-in for a database write; raises ValueError for a bad row."""
    if row.get("amount") is None or row["amount"] < 0:
        raise ValueError(f"bad amount in row {row.get('id')}")
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
