#!/usr/bin/env bash
# Builds the fixture project for the `find-faster-json-library` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "events"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/events/__init__.py)"
cat > src/events/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/events/load.py)"
cat > src/events/load.py <<'__FIXTURE_EOF__'
import json


def load_events(path):
    """Return the events in a JSON Lines file."""
    events = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            events.append(json.loads(line))
    return events
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_load.py)"
cat > tests/test_load.py <<'__FIXTURE_EOF__'
from events.load import load_events


def test_load_events_reads_each_line(tmp_path):
    path = tmp_path / "e.jsonl"
    path.write_text('{"a": 1}\n{"a": 2}\n')
    assert load_events(path) == [{"a": 1}, {"a": 2}]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
