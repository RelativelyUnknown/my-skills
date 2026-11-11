#!/usr/bin/env bash
# Builds the fixture project for the `request-metrics-bounded-labels` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/api/__init__.py)"
cat > src/api/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/api/app.py)"
cat > src/api/app.py <<'__FIXTURE_EOF__'
import time


def lookup(method: str, path: str) -> tuple[str, int]:
    """Stand-in router: returns (route template, status)."""
    if path.startswith("/orders/"):
        return "/orders/{id}", 200
    return "/unknown", 404


def handle(method: str, path: str) -> int:
    start = time.perf_counter()
    route, status = lookup(method, path)
    time.sleep(0.001)
    _ = time.perf_counter() - start
    return status
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
