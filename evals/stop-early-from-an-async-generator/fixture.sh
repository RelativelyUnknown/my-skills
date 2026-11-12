#!/usr/bin/env bash
# Builds the fixture project for the `stop-early-from-an-async-generator` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "store"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/store/__init__.py)"
cat > src/store/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/store/rows.py)"
cat > src/store/rows.py <<'__FIXTURE_EOF__'
CLOSED = []


async def rows():
    """Yield rows from a connection that must be closed."""
    try:
        for i in range(1000):
            yield {"id": i}
    finally:
        CLOSED.append(True)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
