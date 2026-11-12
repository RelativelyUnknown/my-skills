#!/usr/bin/env bash
# Builds the fixture project for the `load-settings-house-rules` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "acme"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/acme/__init__.py)"
cat > src/acme/__init__.py <<'__FIXTURE_EOF__'
__all__: list[str] = []
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_import.py)"
cat > tests/test_import.py <<'__FIXTURE_EOF__'
import acme


def test_imports():
    assert acme.__all__ == []
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
