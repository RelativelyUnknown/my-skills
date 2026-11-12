#!/usr/bin/env bash
# Builds the fixture for `seeded-audit-hard`: ten defects that need two or more files read together, and eight look-alikes.
set -euo pipefail
mkdir -p ledger tests
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "ledger"
version = "2.3.0"
requires-python = ">=3.12"
dependencies = ["pyyaml"]
__FIXTURE_EOF__
cat > ledger/__init__.py <<'__FIXTURE_EOF__'
__FIXTURE_EOF__
cat > ledger/settings.py <<'__FIXTURE_EOF__'
import os

DATA_DIR = "/srv/data"
REPORT_DIR = "/srv/reports"
SIGNING_KEY = os.environ["LEDGER_SIGNING_KEY"].encode()
WEBHOOK_SECRET = os.environ["LEDGER_WEBHOOK_SECRET"].encode()
# Development flag.
SKIP_SIG = os.environ.get("LEDGER_SKIP_SIG", "0")
__FIXTURE_EOF__
cat > ledger/models.py <<'__FIXTURE_EOF__'
class User:
    def __init__(self, id, name, email, password_hash, reset_token=None, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.reset_token = reset_token
        self.is_admin = is_admin


class Order:
    def __init__(self, id, owner_id, total, status="new", payment_ref=None):
        self.id = id
        self.owner_id = owner_id
        self.total = total
        self.status = status
        self.payment_ref = payment_ref
__FIXTURE_EOF__
cat > ledger/auth.py <<'__FIXTURE_EOF__'
import time

from ledger import store

_attempts = {}


def require_login(handler):
    def wrapper(request):
        user = store.user_for_session(request.cookies.get("session"))
        if user is None:
            return 401
        return handler(request, user)

    return wrapper


def rate_limited(request):
    key = request.headers.get("X-Forwarded-For", request.remote_addr)
    now = time.time()
    recent = [t for t in _attempts.get(key, []) if now - t < 60]
    recent.append(now)
    _attempts[key] = recent
    return len(recent) > 5


def login(request):
    if rate_limited(request):
        return 429
    user = store.find_by_email(request.json["email"])
    if user and store.check_password(user, request.json["password"]):
        return store.new_session(user)
    return 401


def confirm_reset(request):
    user = store.find_by_email(request.json["email"])
    if user is None:
        return 404
    if request.json.get("token") == user.reset_token:
        store.set_password(user, request.json["new_password"])
        user.reset_token = None
        return 200
    return 403
__FIXTURE_EOF__
cat > ledger/routes.py <<'__FIXTURE_EOF__'
"""Entry points."""
from ledger import accounts, auth, billing, files, jobs, orders, views, webhooks
from ledger.auth import require_login


@require_login
def export(request, user):
    jobs.enqueue({"kind": "export", "user_id": request.json["user_id"], "format": request.json.get("format", "csv")})
    return 202


@require_login
def download(request, user):
    return files.download(request.args["name"])


@require_login
def report(request, user):
    return files.read_report(request.args["path"])


@require_login
def refund(request, user):
    return billing.refund(int(request.args["order"]), user)


@require_login
def update_account(request, user):
    return accounts.update(user, request.json)


@require_login
def summary(request, user):
    return views.account_summary(request, user)


@require_login
def cancel(request, user):
    return orders.cancel(int(request.args["order"]), user)


def pay_webhook(request):
    return webhooks.handle(request)


def login(request):
    return auth.login(request)


def reset(request):
    return auth.confirm_reset(request)
__FIXTURE_EOF__
cat > ledger/jobs.py <<'__FIXTURE_EOF__'
"""Background jobs. Messages are put on the queue by the web process."""
import json

from ledger import store

_queue = []


def enqueue(message):
    _queue.append(json.dumps(message))


def run_export(message):
    rows = store.rows_for_user(message["user_id"])
    return "\n".join(",".join(map(str, r)) for r in rows)


def reconcile(order):
    """Nightly: orders with a payment reference but a stale status are marked shipped."""
    if order.payment_ref and order.status != "shipped":
        order.status = "shipped"


def worker():
    while _queue:
        message = json.loads(_queue.pop(0))
        if message["kind"] == "export":
            run_export(message)
__FIXTURE_EOF__
cat > ledger/files.py <<'__FIXTURE_EOF__'
import os
import unicodedata

from ledger import settings


def download(name):
    if ".." in name or name.startswith("/"):
        raise ValueError("bad name")
    path = os.path.join(settings.DATA_DIR, unicodedata.normalize("NFKC", name))
    with open(path, "rb") as f:
        return f.read()


def read_report(path):
    real = os.path.realpath(path)
    if not real.startswith(settings.REPORT_DIR):
        raise PermissionError(path)
    with open(real, "rb") as f:
        return f.read()
__FIXTURE_EOF__
cat > ledger/billing.py <<'__FIXTURE_EOF__'
from ledger import payments, store


def refund(order_id, user):
    order = store.get_order(order_id)
    if order.owner_id != user.id:
        return 403
    if order.status != "paid":
        return 409
    payments.refund(order.payment_ref, order.total)
    order.status = "refunded"
    store.save(order)
    return 200
__FIXTURE_EOF__
cat > ledger/accounts.py <<'__FIXTURE_EOF__'
from ledger import store


def update(user, data):
    allowed = set(vars(user))
    for key, value in data.items():
        if key in allowed:
            setattr(user, key, value)
    store.save(user)
    return 200
__FIXTURE_EOF__
cat > ledger/orders.py <<'__FIXTURE_EOF__'
from ledger import store

TRANSITIONS = {
    "new": {"paid", "cancelled"},
    "paid": {"shipped", "refunded"},
    "shipped": set(),
    "cancelled": set(),
    "refunded": set(),
}


def advance(order, new_status):
    if new_status not in TRANSITIONS[order.status]:
        raise ValueError(f"{order.status} -> {new_status}")
    order.status = new_status
    store.save(order)


def cancel(order_id, user):
    order = store.get_order(order_id)
    if order.owner_id != user.id:
        return 403
    advance(order, "cancelled")
    return 200
__FIXTURE_EOF__
cat > ledger/webhooks.py <<'__FIXTURE_EOF__'
import hashlib
import hmac

from ledger import settings, store


def handle(request):
    if not settings.SKIP_SIG:
        expected = hmac.new(settings.WEBHOOK_SECRET, request.body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, request.headers.get("X-Signature", "")):
            return 401
    event = request.json
    if event["type"] == "payment.succeeded":
        order = store.get_order(event["order_id"])
        order.status = "paid"
        order.payment_ref = event["reference"]
        store.save(order)
    return 200
__FIXTURE_EOF__
cat > ledger/cache.py <<'__FIXTURE_EOF__'
_store = {}


def get(key):
    return _store.get(key)


def set(key, value):
    _store[key] = value
__FIXTURE_EOF__
cat > ledger/views.py <<'__FIXTURE_EOF__'
from ledger import cache, store


def account_summary(request, user):
    key = request.path
    cached = cache.get(key)
    if cached is not None:
        return cached
    body = {"name": user.name, "email": user.email, "orders": store.rows_for_user(user.id)}
    cache.set(key, body)
    return body
__FIXTURE_EOF__
cat > ledger/misc.py <<'__FIXTURE_EOF__'
import hashlib
import hmac
import ipaddress
import logging
import pickle
import socket
import subprocess
import urllib.request
from urllib.parse import urlparse

import yaml

from ledger import settings

log = logging.getLogger(__name__)
TABLES = {"orders": "orders", "refunds": "refund_log"}


def count_rows(conn, kind, owner_id):
    table = TABLES[kind]
    return conn.execute(f"SELECT COUNT(*) FROM {table} WHERE owner_id = ?", (owner_id,)).fetchone()[0]


def fetch_preview(url):
    host = urlparse(url).hostname
    infos = socket.getaddrinfo(host, 443)
    for info in infos:
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise ValueError("not a public address")
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read(4096)


def thumbnail(filename):
    return subprocess.run(["convert", "--", filename, "-resize", "64x64", "out.png"], check=True)


def load_state(blob, signature):
    expected = hmac.new(settings.SIGNING_KEY, blob, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ValueError("bad signature")
    return pickle.loads(blob)


def load_config(text):
    return yaml.safe_load(text)


def etag(body):
    return hashlib.md5(body).hexdigest()


def call_logged(fn):
    try:
        return fn()
    except Exception:
        log.exception("call failed")
        raise
__FIXTURE_EOF__
cat > ledger/store.py <<'__FIXTURE_EOF__'
"""Persistence stubs used by the rest of the package."""


def user_for_session(session_id): ...
def find_by_email(email): ...
def check_password(user, password): ...
def new_session(user): ...
def set_password(user, password): ...
def get_order(order_id): ...
def save(obj): ...
def rows_for_user(user_id): ...
__FIXTURE_EOF__
cat > ledger/payments.py <<'__FIXTURE_EOF__'
def refund(reference, amount): ...
__FIXTURE_EOF__
cat > tests/helpers.py <<'__FIXTURE_EOF__'
def expected_total(expr):
    return eval(expr)
__FIXTURE_EOF__
git init -q -b main
git add -A
