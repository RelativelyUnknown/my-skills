#!/usr/bin/env bash
# Builds the fixture project for the `debug-order-dependent-test` case in the empty workspace.
set -euo pipefail
mkdir -p src/rates tests
cat > pyproject.toml <<'__F__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "rates"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__F__
cat > src/rates/__init__.py <<'__F__'
from rates.core import convert, load_rates

__all__ = ["convert", "load_rates"]
__F__
cat > src/rates/core.py <<'__F__'
"""Currency rates relative to EUR."""

_DEFAULTS = {"EUR": 1.0, "USD": 1.1, "GBP": 0.85}


def load_rates(overrides=None):
    """Return the rates, with any per-call overrides applied."""
    rates = _DEFAULTS
    if overrides:
        rates.update(overrides)
    return rates


def convert(amount, currency, overrides=None):
    return round(amount * load_rates(overrides)[currency], 2)
__F__
cat > tests/test_convert.py <<'__F__'
from rates import convert


def test_convert_with_override():
    assert convert(10, "USD", {"USD": 2.0}) == 20.0


def test_convert_gbp():
    assert convert(100, "GBP") == 85.0
__F__
cat > tests/test_defaults.py <<'__F__'
from rates import load_rates


def test_default_usd_rate():
    assert load_rates()["USD"] == 1.1
__F__
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -q -m "rates"
