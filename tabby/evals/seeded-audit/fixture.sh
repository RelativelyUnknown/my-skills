#!/usr/bin/env bash
# Builds the fixture for the `seeded-audit` case: three real vulnerabilities and three look-alikes.
set -euo pipefail
mkdir -p app
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "exports"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = []
__FIXTURE_EOF__
cat > app/__init__.py <<'__FIXTURE_EOF__'
__FIXTURE_EOF__
cat > app/routes.py <<'__FIXTURE_EOF__'
"""HTTP entry points. Every value in `request.args` comes from an untrusted client."""
from app import db, fetch, files


def handle(request, conn):
    route = request.path
    if route == "/user":
        return db.find_user(conn, request.args["name"])
    if route == "/orders":
        return db.list_orders(conn, request.args.get("sort", "created"))
    if route == "/download":
        return files.download("/srv/exports", request.args["file"])
    if route == "/invoice":
        return files.read_template(request.args.get("kind", "invoice.txt"))
    if route == "/preview":
        return fetch.preview(request.args["url"])
    if route == "/version":
        return fetch.build_id()
    return 404
__FIXTURE_EOF__
cat > app/db.py <<'__FIXTURE_EOF__'
SORT_COLUMNS = {"created", "total", "status"}


def find_user(conn, name):
    return conn.execute(f"SELECT id, name FROM users WHERE name = '{name}'").fetchall()


def list_orders(conn, sort):
    column = sort if sort in SORT_COLUMNS else "created"
    return conn.execute(f"SELECT id, total FROM orders ORDER BY {column}").fetchall()
__FIXTURE_EOF__
cat > app/files.py <<'__FIXTURE_EOF__'
import os

TEMPLATES = ("invoice.txt", "receipt.txt")


def download(base, filename):
    with open(os.path.join(base, filename), "rb") as f:
        return f.read()


def read_template(name):
    if name not in TEMPLATES:
        raise ValueError(name)
    with open(os.path.join("/srv/templates", name), "rb") as f:
        return f.read()
__FIXTURE_EOF__
cat > app/fetch.py <<'__FIXTURE_EOF__'
import hashlib
import subprocess
import urllib.request


def preview(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read(4096)


def build_id():
    out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    return hashlib.md5(out.stdout.encode()).hexdigest()  # short cache key, not a security control
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
