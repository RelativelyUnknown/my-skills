#!/usr/bin/env bash
# Builds the fixture project for the `first-endpoint-from-a-library` case in the empty workspace.
set -euo pipefail
mkdir -p src/stockroom tests
cat > pyproject.toml <<'__F__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "stockroom"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
__F__
cat > AGENTS.md <<'__F__'
## Tabby
reviewed: 2026-11-01 @ 0000000
purpose: stock lookups and counts for one warehouse, as a Python library
users: the warehouse team, from scripts and notebooks
goals: lookups stay under 5 ms for 100k items
growth: 1. the warehouse tablets will need to call it over HTTP; 2. a second warehouse
workload: read heavy, a few requests per second, 100k items in memory
conventions: plain functions over dataclasses; no global state
out-of-scope: user accounts
constraints: python 3.12+
ask-first: new dependency
kind: library
modules: development
commands: `PYTHONPATH=src python3 -m unittest`
__F__
cat > src/stockroom/__init__.py <<'__F__'
from stockroom.items import Item, lookup_item

__all__ = ["Item", "lookup_item"]
__F__
cat > src/stockroom/items.py <<'__F__'
from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    sku: str
    name: str
    on_hand: int
    cost_price: float  # internal: what we paid, never shown outside the company


def lookup_item(items: dict[str, Item], sku: str) -> Item | None:
    """Return the item with this SKU, or None."""
    return items.get(sku.strip().upper())
__F__
touch tests/__init__.py
cat > tests/test_items.py <<'__F__'
import unittest

from stockroom import Item, lookup_item

ITEMS = {"AB-1": Item("AB-1", "Bolt", 40, 0.12)}


class LookupTest(unittest.TestCase):
    def test_found_ignores_case_and_spaces(self):
        self.assertEqual(lookup_item(ITEMS, " ab-1 ").name, "Bolt")

    def test_missing_is_none(self):
        self.assertIsNone(lookup_item(ITEMS, "ZZ-9"))
__F__
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -q -m "stockroom"
