#!/usr/bin/env bash
# Builds the fixture project for the `gates-multipart-missed-requirement` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# feeds

Pulls partner feeds.

## Configuration

No settings yet.
__FIXTURE_EOF__
mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "feeds"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests", "httpx"]

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/feeds/__init__.py)"
cat > src/feeds/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/feeds/billing.py)"
cat > src/feeds/billing.py <<'__FIXTURE_EOF__'
import requests


def fetch_invoices(base_url: str) -> list[dict]:
    resp = requests.get(f"{base_url}/invoices")
    resp.raise_for_status()
    return resp.json()
__FIXTURE_EOF__
mkdir -p "$(dirname src/feeds/catalog.py)"
cat > src/feeds/catalog.py <<'__FIXTURE_EOF__'
import httpx


def push_item(base_url: str, item: dict) -> None:
    httpx.post(f"{base_url}/items", json=item).raise_for_status()
__FIXTURE_EOF__
mkdir -p "$(dirname src/feeds/legacy.py)"
cat > src/feeds/legacy.py <<'__FIXTURE_EOF__'
import urllib.request


def ping(url: str) -> bytes:
    with urllib.request.urlopen(url) as resp:
        return resp.read()
__FIXTURE_EOF__
mkdir -p "$(dirname scripts/backfill.py)"
cat > scripts/backfill.py <<'__FIXTURE_EOF__'
import requests

for day in range(1, 8):
    requests.post("https://example.invalid/backfill", json={"day": day})
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_billing.py)"
cat > tests/test_billing.py <<'__FIXTURE_EOF__'
from feeds import billing


def test_module_imports():
    assert billing.fetch_invoices
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
