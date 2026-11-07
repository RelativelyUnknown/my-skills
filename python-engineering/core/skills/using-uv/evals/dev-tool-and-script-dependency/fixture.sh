#!/usr/bin/env bash
# Builds the fixture project for the `dev-tool-and-script-dependency` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/__init__.py)"
cat > src/shop/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname uv.lock)"
cat > uv.lock <<'__FIXTURE_EOF__'
version = 1
requires-python = ">=3.12"
__FIXTURE_EOF__
mkdir -p "$(dirname .python-version)"
cat > .python-version <<'__FIXTURE_EOF__'
3.12
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
