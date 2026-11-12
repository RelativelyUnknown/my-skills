#!/usr/bin/env bash
# Builds the fixture project for the `speed-up-matcher` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "matcher"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["."]
__FIXTURE_EOF__
cat > matcher.py <<'__FIXTURE_EOF__'
def match(rows, blocked_ids):
    out = []
    for r in rows:
        if r['id'] not in blocked_ids:  # blocked_ids is a list of ~50k ids
            out.append(r)
    return out
__FIXTURE_EOF__
cat > test_matcher.py <<'__FIXTURE_EOF__'
from matcher import match


def test_match_drops_blocked_ids():
    rows = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert match(rows, [2]) == [{"id": 1}, {"id": 3}]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
