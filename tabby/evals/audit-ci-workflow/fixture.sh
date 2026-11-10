#!/usr/bin/env bash
# Builds the fixture project for the `audit-ci-workflow` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "tinyq"
version = "1.3.0"
requires-python = ">=3.12"

[dependency-groups]
dev = ["pytest>=9"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/tinyq/__init__.py)"
cat > src/tinyq/__init__.py <<'__FIXTURE_EOF__'
__all__ = ["push"]


def push(queue: list[int], item: int) -> None:
    queue.append(item)
__FIXTURE_EOF__
mkdir -p "$(dirname .github/workflows/ci.yml)"
cat > .github/workflows/ci.yml <<'__FIXTURE_EOF__'
name: ci
on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7.0.1
      - uses: astral-sh/setup-uv@v10.3.3
      - run: uv sync --locked
      - run: uv run pytest
__FIXTURE_EOF__
mkdir -p "$(dirname .github/workflows/labeler.yml)"
cat > .github/workflows/labeler.yml <<'__FIXTURE_EOF__'
name: label and smoke-test
on:
  pull_request_target:
    types: [opened, synchronize, edited]

jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7.0.1
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - uses: astral-sh/setup-uv@v10.3.3
      - name: Install and test
        env:
          TEST_PYPI_TOKEN: ${{ secrets.TEST_PYPI_TOKEN }}
        run: |
          uv sync
          uv run pytest
      - name: Log the title
        run: |
          echo "Checked: ${{ github.event.pull_request.title }}"
__FIXTURE_EOF__
mkdir -p "$(dirname .github/workflows/release.yml)"
cat > .github/workflows/release.yml <<'__FIXTURE_EOF__'
name: release
on:
  push:
    tags: ["v*"]

permissions: {}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v7.0.1
      - uses: astral-sh/setup-uv@v10.3.3
      - run: uv build
      - uses: actions/upload-artifact@v7.0.2
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v8.0.2
        with:
          name: dist
          path: dist/
      - uses: pypa/gh-action-pypi-publish@release/v1
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
