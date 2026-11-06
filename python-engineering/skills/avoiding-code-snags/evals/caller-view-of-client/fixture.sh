#!/usr/bin/env bash
# Builds the fixture project for the `caller-view-of-client` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname src/api/client.py)"
cat > src/api/client.py <<'__FIXTURE_EOF__'
"""HTTP client helpers."""
import functools
import json
import os
from datetime import datetime
from typing import Any, Literal
from urllib.request import urlopen

DEFAULT_TIMEOUT = 30
MAX_BODY_BYTES = 1_000_000

CONFIG = json.load(open("config.json"))
API_KEY = os.environ["API_KEY"]


def retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except OSError:
                if attempt == 2:
                    raise

    return wrapper


@retry
def fetch(url, timeout=DEFAULT_TIMEOUT, retries=None):
    retries = retries or 3
    body = urlopen(url).read(MAX_BODY_BYTES)
    return json.loads(body)


def fetch_text(url, *, timeout: float = 30) -> str:
    with urlopen(url, timeout=timeout) as resp:
        return resp.read(MAX_BODY_BYTES).decode()


def request(url, **kwargs):
    return urlopen(url, **kwargs)


def stamp(now=datetime.now()):
    return now.isoformat()


def parse(data, mode="strict"):
    if mode == "strict":
        return json.loads(data)
    return json.loads(data or "{}")


def parse_typed(data: str, mode: Literal["strict", "lenient"] = "strict") -> Any:
    return parse(data, mode)


def get_item(id, type="json") -> dict:
    return {"id": id, "type": type}


def create_user(name, email, phone, address, city, country, zip_code):
    return {"name": name, "email": email, "phone": phone, "address": address,
            "city": city, "country": country, "zip": zip_code}


def read_notes(path):
    with open(path) as f:
        return f.read()


def check(resp, items):
    if resp.status != 200:
        raise Exception("bad status")
    return items[:37]
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
