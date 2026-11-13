#!/usr/bin/env bash
# Builds the fixture project for the `fix-ssrf-in-link-preview` case in the empty workspace.
set -euo pipefail
mkdir -p src/preview tests
cat > pyproject.toml <<'__F__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "preview"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
__F__
cat > src/preview/__init__.py <<'__F__'
from preview.fetch import fetch_preview

__all__ = ["fetch_preview"]
__F__
cat > src/preview/fetch.py <<'__F__'
"""Fetch a page a user linked to and return its title for a preview card."""
import re
import urllib.request

BLOCKED = ("localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254")


class BlockedUrl(ValueError):
    pass


def fetch_preview(url, *, opener=urllib.request.urlopen):
    if not url.startswith(("http://", "https://")):
        raise BlockedUrl("only http and https")
    if any(b in url for b in BLOCKED):
        raise BlockedUrl("internal address")
    with opener(url, timeout=5) as resp:
        html = resp.read(200_000).decode("utf-8", "replace")
    match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    return {"url": url, "title": match.group(1).strip() if match else ""}
__F__
touch tests/__init__.py
cat > tests/test_fetch.py <<'__F__'
import io
import unittest

from preview import fetch_preview
from preview.fetch import BlockedUrl


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def fake_opener(url, timeout=None):
    return FakeResponse(b"<html><title> Example </title></html>")


class FetchTest(unittest.TestCase):
    def test_returns_title(self):
        self.assertEqual(fetch_preview("https://example.com/", opener=fake_opener)["title"], "Example")

    def test_rejects_other_schemes(self):
        with self.assertRaises(BlockedUrl):
            fetch_preview("file:///etc/passwd", opener=fake_opener)

    def test_rejects_localhost(self):
        with self.assertRaises(BlockedUrl):
            fetch_preview("http://localhost/admin", opener=fake_opener)
__F__
git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -q -m "preview"
