#!/usr/bin/env bash
# Fixture for `seeded-audit-hard-b`: ten defects that need two or more files read together, and eight look-alikes.
set -euo pipefail
mkdir -p clinic tests
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "clinic"
version = "0.9.0"
requires-python = ">=3.12"
dependencies = ["pyyaml"]
__FIXTURE_EOF__
cat > clinic/__init__.py <<'__FIXTURE_EOF__'
__FIXTURE_EOF__
cat > clinic/config.py <<'__FIXTURE_EOF__'
import os

UPLOAD_DIR = "/var/clinic/uploads"
SECRET = os.environ["CLINIC_SECRET"].encode()
LINK_KEY = os.environ["CLINIC_LINK_KEY"].encode()
ALLOW_UNSIGNED = os.environ.get("CLINIC_ALLOW_UNSIGNED", "false")
HOME_HOST = "clinic.example"
OTP_LIMIT = 5
__FIXTURE_EOF__
cat > clinic/models.py <<'__FIXTURE_EOF__'
class Patient:
    def __init__(self, id, name, phone, role="patient", pending_otp=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.role = role
        self.pending_otp = pending_otp


class Appointment:
    def __init__(self, id, patient_id, slot, status="requested"):
        self.id = id
        self.patient_id = patient_id
        self.slot = slot
        self.status = status


class Voucher:
    def __init__(self, code, balance):
        self.code = code
        self.balance = balance
__FIXTURE_EOF__
cat > clinic/handlers.py <<'__FIXTURE_EOF__'
"""Request handlers."""
from clinic import accounts, links, media, reports, schedule, vouchers
from clinic.auth import logged_in


@logged_in
def request_summary(request, patient):
    reports.enqueue({"kind": "summary", "patient_id": request.json["patient_id"]})
    return 202


@logged_in
def upload(request, patient):
    return media.save_upload(request.args["name"], request.files["file"].read())


@logged_in
def go(request, patient):
    return links.redirect_to(request.args["next"])


@logged_in
def redeem(request, patient):
    return vouchers.redeem(request.args["code"], int(request.args["amount"]))


def verify_code(request):
    return accounts.verify_otp(request)


@logged_in
def edit_profile(request, patient):
    return accounts.edit(patient, request.json)


@logged_in
def my_schedule(request, patient):
    return schedule.view(request, patient)


@logged_in
def shared_link(request, patient):
    return links.open_shared(request.args["token"], request.args["sig"])
__FIXTURE_EOF__
cat > clinic/auth.py <<'__FIXTURE_EOF__'
from clinic import db


def logged_in(handler):
    def wrapper(request):
        patient = db.patient_for_token(request.headers.get("Authorization"))
        if patient is None:
            return 401
        return handler(request, patient)

    return wrapper
__FIXTURE_EOF__
cat > clinic/accounts.py <<'__FIXTURE_EOF__'
from clinic import config, db

_tries = {}


def verify_otp(request):
    device = request.cookies.get("device_id", "")
    _tries[device] = _tries.get(device, 0) + 1
    if _tries[device] > config.OTP_LIMIT:
        return 429
    patient = db.find_by_phone(request.json["phone"])
    if patient is None:
        return 404
    if request.json.get("code") == patient.pending_otp:
        patient.pending_otp = None
        return db.new_token(patient)
    return 403


def edit(patient, data):
    for key, value in data.items():
        if hasattr(patient, key):
            setattr(patient, key, value)
    db.save(patient)
    return 200
__FIXTURE_EOF__
cat > clinic/reports.py <<'__FIXTURE_EOF__'
import json

from clinic import db

_queue = []


def enqueue(message):
    _queue.append(json.dumps(message))


def build_summary(message):
    return db.appointments_for(message["patient_id"])


def work():
    while _queue:
        message = json.loads(_queue.pop(0))
        if message["kind"] == "summary":
            build_summary(message)
__FIXTURE_EOF__
cat > clinic/media.py <<'__FIXTURE_EOF__'
import os
from urllib.parse import unquote

from clinic import config


def save_upload(name, data):
    if ".." in name or "/" in name or "\\" in name:
        raise ValueError("bad name")
    path = os.path.join(config.UPLOAD_DIR, unquote(name))
    with open(path, "wb") as f:
        f.write(data)
    return path
__FIXTURE_EOF__
cat > clinic/links.py <<'__FIXTURE_EOF__'
import hashlib
import hmac
from urllib.parse import urlparse

from clinic import config, db


def redirect_to(target):
    host = urlparse(target).hostname or ""
    if not host.endswith(config.HOME_HOST):
        raise ValueError("external redirect")
    return 302, target


def open_shared(token, sig):
    if config.ALLOW_UNSIGNED or hmac.compare_digest(
        hmac.new(config.LINK_KEY, token.encode(), hashlib.sha256).hexdigest(), sig
    ):
        return db.document_for_token(token)
    return 403
__FIXTURE_EOF__
cat > clinic/vouchers.py <<'__FIXTURE_EOF__'
from clinic import db, gateway


def redeem(code, amount):
    voucher = db.get_voucher(code)
    if voucher.balance < amount:
        return 409
    gateway.charge_partner(code, amount)
    voucher.balance -= amount
    db.save(voucher)
    return 200
__FIXTURE_EOF__
cat > clinic/schedule.py <<'__FIXTURE_EOF__'
from clinic import cache, db

TRANSITIONS = {
    "requested": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def move(appointment, new_status):
    if new_status not in TRANSITIONS[appointment.status]:
        raise ValueError(f"{appointment.status} -> {new_status}")
    appointment.status = new_status
    db.save(appointment)


def view(request, patient):
    key = (request.path, request.args.get("week", ""))
    hit = cache.get(key)
    if hit is not None:
        return hit
    body = {"patient": patient.name, "appointments": db.appointments_for(patient.id)}
    cache.set(key, body)
    return body
__FIXTURE_EOF__
cat > clinic/cache.py <<'__FIXTURE_EOF__'
_data = {}


def get(key):
    return _data.get(key)


def set(key, value):
    _data[key] = value
__FIXTURE_EOF__
cat > clinic/jobs.py <<'__FIXTURE_EOF__'
"""Scheduled jobs."""
from clinic import db


def import_calendar(rows):
    for row in rows:
        appointment = db.get_appointment(row["id"])
        appointment.status = "confirmed"
        db.save(appointment)


def mark_past_completed(now):
    for appointment in db.appointments_before(now):
        appointment.status = "completed"
        db.save(appointment)
__FIXTURE_EOF__
cat > clinic/util.py <<'__FIXTURE_EOF__'
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

from clinic import config

log = logging.getLogger(__name__)
KINDS = {"appointments": "appointments", "vouchers": "voucher_log"}


def count(conn, kind, patient_id):
    table = KINDS[kind]
    return conn.execute(f"SELECT COUNT(*) FROM {table} WHERE patient_id = ?", (patient_id,)).fetchone()[0]


def fetch_logo(url):
    host = urlparse(url).hostname
    for info in socket.getaddrinfo(host, 443):
        if not ipaddress.ip_address(info[4][0]).is_global:
            raise ValueError("not public")
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read(65536)


def make_thumb(filename):
    return subprocess.run(["convert", "--", filename, "-resize", "96x96", "thumb.png"], check=True)


def load_session(blob, sig):
    expected = hmac.new(config.SECRET, blob, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        raise ValueError("bad signature")
    return pickle.loads(blob)


def load_templates(text):
    return yaml.safe_load(text)


def etag(body):
    return hashlib.md5(body).hexdigest()


def with_logging(fn):
    try:
        return fn()
    except Exception:
        log.exception("failed")
        raise
__FIXTURE_EOF__
cat > clinic/db.py <<'__FIXTURE_EOF__'
def patient_for_token(token): ...
def find_by_phone(phone): ...
def new_token(patient): ...
def save(obj): ...
def appointments_for(patient_id): ...
def appointments_before(now): ...
def get_appointment(appointment_id): ...
def get_voucher(code): ...
def document_for_token(token): ...
__FIXTURE_EOF__
cat > clinic/gateway.py <<'__FIXTURE_EOF__'
def charge_partner(code, amount): ...
__FIXTURE_EOF__
cat > tests/helpers.py <<'__FIXTURE_EOF__'
def expected(expr):
    return eval(expr)
__FIXTURE_EOF__
git init -q -b main
git add -A
