#!/usr/bin/env bash
# Builds the fixture project for the `literal-defaults-fetch-json` case in the empty workspace.
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
mkdir -p "$(dirname src/api/client.py)"
cat > src/api/client.py <<'__FIXTURE_EOF__'
"""Small HTTP helpers."""
from urllib.request import urlopen


def ping(url):
    """Return True when url answers."""
    with urlopen(url, timeout=5) as resp:
        return resp.status == 200
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_client.py)"
cat > tests/test_client.py <<'__FIXTURE_EOF__'
import json

from api.client import ping


def test_ping_file_url(tmp_path):
    path = tmp_path / "x.json"
    path.write_text(json.dumps({"a": 1}))
    assert ping(path.as_uri()) is False or True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
