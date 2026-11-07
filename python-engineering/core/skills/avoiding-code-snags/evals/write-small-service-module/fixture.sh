#!/usr/bin/env bash
# Builds the fixture project for the `write-small-service-module` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# orders

Small order-handling helpers.
__FIXTURE_EOF__
mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "orders"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/orders/__init__.py)"
cat > src/orders/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
