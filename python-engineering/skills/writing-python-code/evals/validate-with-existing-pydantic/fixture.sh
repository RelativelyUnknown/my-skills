#!/usr/bin/env bash
# Builds the fixture project for the `validate-with-existing-pydantic` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "catalog"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pydantic>=2"]

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/catalog/__init__.py)"
cat > src/catalog/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/catalog/models.py)"
cat > src/catalog/models.py <<'__FIXTURE_EOF__'
from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(min_length=1)
    email: str
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_models.py)"
cat > tests/test_models.py <<'__FIXTURE_EOF__'
from catalog.models import User


def test_user():
    assert User(name="a", email="a@b.c").name == "a"
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
