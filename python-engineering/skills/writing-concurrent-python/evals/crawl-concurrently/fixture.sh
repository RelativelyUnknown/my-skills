#!/usr/bin/env bash
# Builds the fixture project for the `crawl-concurrently` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "fetcher"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/fetcher/__init__.py)"
cat > src/fetcher/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/fetcher/crawl.py)"
cat > src/fetcher/crawl.py <<'__FIXTURE_EOF__'
import time


def fetch(url):
    """Blocking call, about one second each. Not ours to change."""
    time.sleep(1)
    if url.endswith("/bad"):
        raise ConnectionError(url)
    return f"body of {url}"


def crawl(urls):
    results = {}
    for url in urls:
        results[url] = fetch(url)
    return results
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
