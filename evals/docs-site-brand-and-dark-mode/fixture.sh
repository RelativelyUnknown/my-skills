#!/usr/bin/env bash
# Builds the fixture project for the `docs-site-brand-and-dark-mode` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# lintkit

Docs live in docs/ and build with `mkdocs build`.
__FIXTURE_EOF__
mkdir -p "$(dirname mkdocs.yml)"
cat > mkdocs.yml <<'__FIXTURE_EOF__'
site_name: lintkit
theme:
  name: material
nav:
  - Home: index.md
  - Guide: guide.md
__FIXTURE_EOF__
mkdir -p "$(dirname docs/index.md)"
cat > docs/index.md <<'__FIXTURE_EOF__'
# lintkit

A small linter for config files.
__FIXTURE_EOF__
mkdir -p "$(dirname docs/guide.md)"
cat > docs/guide.md <<'__FIXTURE_EOF__'
# Guide

Install with `pip install lintkit`, then run `lintkit check .`.
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
