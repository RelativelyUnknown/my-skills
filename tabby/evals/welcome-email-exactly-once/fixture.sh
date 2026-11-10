#!/usr/bin/env bash
# Builds the fixture project for the `welcome-email-exactly-once` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mail"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/mail/__init__.py)"
cat > src/mail/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/mail/db.py)"
cat > src/mail/db.py <<'__FIXTURE_EOF__'
import sqlite3


def connect(path: str = "app.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path, isolation_level=None)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, welcome_sent_at TEXT)"
    )
    return conn
__FIXTURE_EOF__
mkdir -p "$(dirname src/mail/smtp.py)"
cat > src/mail/smtp.py <<'__FIXTURE_EOF__'
SENT: list[tuple[str, str]] = []


def send(to: str, subject: str) -> None:
    """Stand-in for the mail server."""
    SENT.append((to, subject))
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
