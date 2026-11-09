#!/usr/bin/env bash
# Builds the fixture project for the `batches-and-utc` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "orders"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/db.py)"
cat > src/orders/db.py <<'__FIXTURE_EOF__'
def save_batch(batch: list[dict]) -> None:
    """Persist one batch of rows."""
    raise NotImplementedError("wired up in deployment")
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/ingest.py)"
cat > src/orders/ingest.py <<'__FIXTURE_EOF__'
def ingest(rows: list[dict]) -> None:
    """Save rows to the database."""
    raise NotImplementedError
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_ingest.py)"
cat > tests/test_ingest.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
