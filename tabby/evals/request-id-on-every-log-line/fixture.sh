#!/usr/bin/env bash
# Builds the fixture project for the `request-id-on-every-log-line` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "svc"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/svc/__init__.py)"
cat > src/svc/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/svc/service.py)"
cat > src/svc/service.py <<'__FIXTURE_EOF__'
import asyncio
import logging

log = logging.getLogger(__name__)


def audit(order_id: int) -> None:
    log.info("audited order %s", order_id)


async def handle_request(order_id: int) -> None:
    log.info("handling order %s", order_id)
    await asyncio.to_thread(audit, order_id)
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_placeholder.py)"
cat > tests/test_placeholder.py <<'__FIXTURE_EOF__'
def test_placeholder():
    assert True
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
