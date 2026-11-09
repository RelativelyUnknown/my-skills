#!/usr/bin/env bash
# Builds the fixture project for the `settings-loaded-at-startup` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/app/__init__.py)"
cat > src/app/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/app/main.py)"
cat > src/app/main.py <<'__FIXTURE_EOF__'
def run() -> None:
    """Start the service."""
    print("running")


if __name__ == "__main__":
    run()
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
