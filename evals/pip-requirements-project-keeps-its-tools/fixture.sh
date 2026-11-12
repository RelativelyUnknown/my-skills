#!/usr/bin/env bash
# Builds the fixture project for the `pip-requirements-project-keeps-its-tools` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname requirements.txt)"
cat > requirements.txt <<'__FIXTURE_EOF__'
requests-cache==1.2.1
__FIXTURE_EOF__
mkdir -p "$(dirname requirements-dev.txt)"
cat > requirements-dev.txt <<'__FIXTURE_EOF__'
-r requirements.txt
pytest==8.3.3
flake8==7.1.1
__FIXTURE_EOF__
mkdir -p "$(dirname setup.cfg)"
cat > setup.cfg <<'__FIXTURE_EOF__'
[metadata]
name = pricewatch
version = 0.3.1

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.10
install_requires =
    requests-cache==1.2.1

[options.packages.find]
where = src

[flake8]
max-line-length = 100
__FIXTURE_EOF__
mkdir -p "$(dirname setup.py)"
cat > setup.py <<'__FIXTURE_EOF__'
from setuptools import setup

setup()
__FIXTURE_EOF__
mkdir -p "$(dirname tox.ini)"
cat > tox.ini <<'__FIXTURE_EOF__'
[tox]
envlist = py310, py312

[testenv]
deps = -rrequirements-dev.txt
commands = pytest
__FIXTURE_EOF__
mkdir -p "$(dirname src/pricewatch/__init__.py)"
cat > src/pricewatch/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/pricewatch/client.py)"
cat > src/pricewatch/client.py <<'__FIXTURE_EOF__'
import json
import urllib.request


def fetch_prices(url: str) -> dict[str, float]:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.load(response)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_client.py)"
cat > tests/test_client.py <<'__FIXTURE_EOF__'
from pricewatch.client import fetch_prices


def test_is_callable():
    assert callable(fetch_prices)
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
