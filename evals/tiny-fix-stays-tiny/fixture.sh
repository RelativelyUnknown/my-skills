#!/usr/bin/env bash
# Builds the fixture project for the `tiny-fix-stays-tiny` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "textkit"
version = "0.5.1"
requires-python = ">=3.11"

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/textkit/__init__.py)"
cat > src/textkit/__init__.py <<'__FIXTURE_EOF__'
from textkit.wrap import wrap

__all__ = ["wrap"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/textkit/utils.py)"
cat > src/textkit/utils.py <<'__FIXTURE_EOF__'
def chunks(words, width):
    line = []
    for word in words:
        if line and len(" ".join(line + [word])) > width:
            yield " ".join(line)
            line = []
        line.append(word)
    if line:
        yield " ".join(line)
__FIXTURE_EOF__
mkdir -p "$(dirname src/textkit/wrap.py)"
cat > src/textkit/wrap.py <<'__FIXTURE_EOF__'
from textkit.utils import chunks

DEFAULT_WIDTH = 72


def wrap(text, width=DEFAULT_WIDTH):
    if width <= 0:
        raise ValueError(f"width must be postive, got {width}")
    return list(chunks(text.split(), width))
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_wrap.py)"
cat > tests/test_wrap.py <<'__FIXTURE_EOF__'
import pytest

from textkit import wrap


def test_wraps_at_width():
    assert wrap("aa bb cc", 5) == ["aa bb", "cc"]


def test_rejects_zero_width():
    with pytest.raises(ValueError, match="width must be"):
        wrap("aa", 0)
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
