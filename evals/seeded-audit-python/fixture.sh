#!/usr/bin/env bash
# Builds the fixture for `seeded-audit-python`: twelve planted defects and eight look-alikes in a small shop backend.
set -euo pipefail
mkdir -p shop tests
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "shop"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = ["pyjwt", "pyyaml", "jinja2"]
__FIXTURE_EOF__
cat > shop/__init__.py <<'__FIXTURE_EOF__'
__FIXTURE_EOF__
cat > shop/routes.py <<'__FIXTURE_EOF__'
"""HTTP entry points. Everything in `request.args`, `request.json`, `request.files` and headers comes from an untrusted client."""
from shop import accounts, billing, db, media, orders, webhooks


def handle(request, conn, user):
    p = request.path
    if p == "/users/search":
        return db.search_users(conn, request.args["q"])
    if p == "/users/by-id":
        return db.get_user_by_id(conn, int(request.args["id"]))
    if p == "/invoice":
        return billing.get_invoice(conn, int(request.args["id"]))
    if p == "/profile":
        return accounts.update_profile(conn, user, request.json)
    if p == "/prefs/import":
        return accounts.load_prefs(request.files["prefs"].read())
    if p == "/avatar":
        return media.fetch_avatar(request.args["url"])
    if p == "/themes/upload":
        return media.install_theme(request.files["theme"], "/srv/themes")
    if p == "/withdraw":
        return billing.withdraw(conn, user["id"], int(request.args["amount"]))
    if p == "/rates":
        return billing.fetch_rates()
    if p == "/pay/webhook":
        return webhooks.handle_webhook(conn, request.json)
    if p == "/orders/ship":
        return orders.ship_order(conn, int(request.args["id"]))
    if p == "/banner":
        return media.banner()
    if p == "/receipt":
        return media.render_receipt(request.args.get("name", ""))
    if p == "/login/token":
        return accounts.check_token(request.headers["X-Token"], user["token"])
    if p == "/me":
        return accounts.whoami(request.headers["Authorization"])
    if p == "/version":
        return media.build_id()
    return 404
__FIXTURE_EOF__
cat > shop/db.py <<'__FIXTURE_EOF__'
def search_users(conn, q):
    return conn.execute(f"SELECT id, name FROM users WHERE name LIKE '%{q}%'").fetchall()


def get_user_by_id(conn, user_id):
    return conn.execute("SELECT id, name FROM users WHERE id = ?", (user_id,)).fetchone()
__FIXTURE_EOF__
cat > shop/billing.py <<'__FIXTURE_EOF__'
import urllib.request

from shop import settings


def get_invoice(conn, invoice_id):
    row = conn.execute("SELECT id, owner_id, total, lines FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    return row


def withdraw(conn, user_id, amount):
    balance = conn.execute("SELECT balance FROM wallets WHERE user_id = ?", (user_id,)).fetchone()[0]
    if balance < amount:
        raise ValueError("insufficient funds")
    conn.execute("UPDATE wallets SET balance = ? WHERE user_id = ?", (balance - amount, user_id))
    return balance - amount


def fetch_rates():
    with urllib.request.urlopen(settings.RATES_URL, timeout=5) as response:
        return response.read()
__FIXTURE_EOF__
cat > shop/accounts.py <<'__FIXTURE_EOF__'
import pickle

import jwt

from shop import settings


def update_profile(conn, user, data):
    user.update(**data)
    conn.execute(
        "UPDATE users SET name = ?, email = ?, is_admin = ? WHERE id = ?",
        (user["name"], user["email"], user.get("is_admin", 0), user["id"]),
    )
    return user


def load_prefs(blob):
    return pickle.loads(blob)


def check_token(supplied, stored):
    return supplied == stored


def whoami(authorization):
    token = authorization.removeprefix("Bearer ")
    algorithm = jwt.get_unverified_header(token)["alg"]
    return jwt.decode(token, settings.JWT_KEY, algorithms=[algorithm])
__FIXTURE_EOF__
cat > shop/media.py <<'__FIXTURE_EOF__'
import hashlib
import random
import subprocess
import tarfile
import urllib.request

from jinja2 import Environment

env = Environment(autoescape=True)

BANNERS = ["Spring sale", "Free shipping over 50", "New arrivals"]


def fetch_avatar(url):
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read(1 << 20)


def install_theme(upload, dest):
    with tarfile.open(fileobj=upload.stream) as archive:
        archive.extractall(dest)


def banner():
    return random.choice(BANNERS)


def render_receipt(name):
    return env.from_string("<p>Thank you, {{ name }}</p>").render(name=name)


def build_id():
    out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    return hashlib.md5(out.stdout.encode()).hexdigest()  # short cache key, not a security control
__FIXTURE_EOF__
cat > shop/orders.py <<'__FIXTURE_EOF__'
VALID = {"new": {"paid", "cancelled"}, "paid": {"shipped", "refunded"}}


def ship_order(conn, order_id):
    status = conn.execute("SELECT status FROM orders WHERE id = ?", (order_id,)).fetchone()[0]
    if status == "shipped":
        raise ValueError("already shipped")
    conn.execute("UPDATE orders SET status = 'shipped' WHERE id = ?", (order_id,))
    return "shipped"


def cancel_order(conn, order_id):
    status = conn.execute("SELECT status FROM orders WHERE id = ?", (order_id,)).fetchone()[0]
    if "cancelled" not in VALID.get(status, set()):
        raise ValueError(status)
    conn.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
__FIXTURE_EOF__
cat > shop/webhooks.py <<'__FIXTURE_EOF__'
from shop import settings


def check_key(supplied):
    if not settings.API_KEY:
        return True
    return supplied == settings.API_KEY


def handle_webhook(conn, payload):
    """Called by the payment provider; `payload` is the parsed JSON body."""
    if payload.get("event") == "payment.succeeded":
        conn.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (payload["order_id"],))
    return "ok"
__FIXTURE_EOF__
cat > shop/settings.py <<'__FIXTURE_EOF__'
import os

import yaml

RATES_URL = "https://rates.example.com/v1/latest"
JWT_KEY = os.environ.get("JWT_KEY", "")
API_KEY = os.environ.get("SHOP_API_KEY", "")

with open(os.path.join(os.path.dirname(__file__), "defaults.yaml")) as f:
    DEFAULTS = yaml.safe_load(f)
__FIXTURE_EOF__
cat > shop/defaults.yaml <<'__FIXTURE_EOF__'
currency: EUR
page_size: 20
__FIXTURE_EOF__
cat > tests/test_helpers.py <<'__FIXTURE_EOF__'
import subprocess


def run_shell(cmd):
    """Test helper only: runs fixed commands written in the tests."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def build_expected(expr):
    return eval(expr)  # expressions below are literals in this file
__FIXTURE_EOF__
git init -q -b main
git add -A
