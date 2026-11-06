#!/usr/bin/env bash
# Builds the fixture project for the `review-new-snag-candidates` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname src/svc/handlers.py)"
cat > src/svc/handlers.py <<'__FIXTURE_EOF__'
"""Request handlers for the billing service."""
import logging
import random
import subprocess
import time
import urllib.request
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)
CHARS = "abcdefghijklmnopqrstuvwxyz0123456789"


def load(path, as_list=False):
    rows = _read(path)
    return rows if as_list else {r["id"]: r for r in rows}


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return [{"id": i, "name": line.strip()} for i, line in enumerate(fh)]


def create_account(payload: dict):
    name = payload.get("name", "")
    plan = payload.get("plan", "free")
    return {"name": name, "plan": plan}


def set_limit(amount):
    if not amount:
        raise ValueError("amount is required")
    return amount


class Cart:
    items = []

    def add(self, item):
        self.items.append(item)


@dataclass
class Credentials:
    user: str
    token: str


def connect(creds: Credentials):
    logger.info("connecting with %s", creds)
    return creds.user


class Account:
    def __init__(self, owner, client):
        self._owner = owner
        self._client = client

    def get_owner(self):
        return self._owner

    def set_owner(self, owner):
        self._owner = owner

    @property
    def balance(self):
        return self._client.fetch_balance(self._owner)

    @property
    def display_name(self):
        return self._owner.title()


def call_with_retry(call):
    while True:
        try:
            return call()
        except Exception:
            time.sleep(1)


async def refresh(url):
    time.sleep(2)
    return urllib.request.urlopen(url, timeout=10).read()


def normalize(rows):
    for row in rows:
        row["name"] = row["name"].strip()
    return rows


def import_file(paths: Optional[List[str]] = None):
    for path in paths or []:
        try:
            _read(path)
        except OSError as e:
            logger.error(str(e))


def thumbnail(filename):
    subprocess.run(f"convert {filename} -resize 64x64 out.png", shell=True, check=True)


def new_token():
    return "".join(random.choice(CHARS) for _ in range(32))


def find_user(users, user_id):
    """Return the user with this id, or None when there is none."""
    try:
        return users[user_id]
    except KeyError:
        return None


def fetch_report(url: str, timeout: float = 30) -> bytes:
    return urllib.request.urlopen(url, timeout=timeout).read()
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
