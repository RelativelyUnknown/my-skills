#!/usr/bin/env bash
# Builds the fixture project for the `one-settings-object` case in the empty workspace.
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
mkdir -p "$(dirname src/shop/client.py)"
cat > src/shop/client.py <<'__FIXTURE_EOF__'
import os


def request_options():
    return {"timeout": float(os.environ.get("TIMEOUT", "30")), "retries": int(os.environ.get("RETRIES", "3"))}


def base_url():
    return os.environ["API_URL"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/db.py)"
cat > src/shop/db.py <<'__FIXTURE_EOF__'
import os
import sqlite3


def connect():
    return sqlite3.connect(os.environ["DATABASE_URL"])
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/mailer.py)"
cat > src/shop/mailer.py <<'__FIXTURE_EOF__'
import os


def sender():
    return os.environ.get("MAIL_FROM", "shop@example.com")
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_basic.py)"
cat > tests/test_basic.py <<'__FIXTURE_EOF__'
from shop.client import base_url, request_options
from shop.mailer import sender


def test_request_options_defaults(monkeypatch):
    monkeypatch.delenv("TIMEOUT", raising=False)
    monkeypatch.delenv("RETRIES", raising=False)
    assert request_options() == {"timeout": 30.0, "retries": 3}


def test_base_url_reads_env(monkeypatch):
    monkeypatch.setenv("API_URL", "https://api.example.com")
    assert base_url() == "https://api.example.com"


def test_sender_default(monkeypatch):
    monkeypatch.delenv("MAIL_FROM", raising=False)
    assert sender() == "shop@example.com"
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
