---
type: regex
target:
  source: file
  path: "tests/test_main.py"
pattern: "setenv|monkeypatch|environ|load\\("
weight: 1
---

Tests for the loader exist
