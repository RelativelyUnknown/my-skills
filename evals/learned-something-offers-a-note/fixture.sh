#!/usr/bin/env bash
# Builds the fixture project for the `learned-something-offers-a-note` case in the empty workspace.
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

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/app/__init__.py)"
cat > src/app/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/app/orm.py)"
cat > src/app/orm.py <<'__FIXTURE_EOF__'
# stands in for a heavy ORM import: slow to import, opens connections on import in the real project
import time

time.sleep(0.2)
Base = object
__FIXTURE_EOF__
mkdir -p "$(dirname src/app/config.py)"
cat > src/app/config.py <<'__FIXTURE_EOF__'
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    api_url: str


def load() -> Settings:
    return Settings(api_url=os.environ.get("API_URL", "http://localhost:9000"))
__FIXTURE_EOF__
mkdir -p "$(dirname src/app/client.py)"
cat > src/app/client.py <<'__FIXTURE_EOF__'
import urllib.request

from app.config import load


def get(path: str) -> bytes:
    settings = load()
    with urllib.request.urlopen(settings.api_url + path) as response:
        return response.read()
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_import_isolation.py)"
cat > tests/test_import_isolation.py <<'__FIXTURE_EOF__'
import subprocess
import sys


def test_config_does_not_import_the_orm():
    """The CLI loads config before anything else; importing app.orm costs 0.2 s and opens connections."""
    code = "import sys, app.config; sys.exit(1 if 'app.orm' in sys.modules else 0)"
    assert subprocess.run([sys.executable, "-c", code]).returncode == 0
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
