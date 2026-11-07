#!/usr/bin/env bash
# Builds the fixture project for the `payment-strategy` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "payments"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/payments/__init__.py)"
cat > src/payments/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/payments/core.py)"
cat > src/payments/core.py <<'__FIXTURE_EOF__'
def process_payment(kind, amount, details):
    if kind == "card":
        fee = amount * 0.029 + 0.30
        return {"status": "ok", "fee": round(fee, 2), "ref": f"card-{details['last4']}"}
    elif kind == "paypal":
        fee = amount * 0.034 + 0.35
        return {"status": "ok", "fee": round(fee, 2), "ref": f"pp-{details['email']}"}
    elif kind == "bank":
        fee = 0.8
        return {"status": "ok", "fee": fee, "ref": f"ach-{details['account']}"}
    else:
        raise ValueError(f"unknown payment kind {kind!r}")
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_core.py)"
cat > tests/test_core.py <<'__FIXTURE_EOF__'
import pytest

from payments.core import process_payment


def test_card_fee_and_reference():
    assert process_payment("card", 100.0, {"last4": "4242"}) == {"status": "ok", "fee": 3.2, "ref": "card-4242"}


def test_paypal_fee_and_reference():
    assert process_payment("paypal", 100.0, {"email": "a@b.c"}) == {"status": "ok", "fee": 3.75, "ref": "pp-a@b.c"}


def test_bank_flat_fee():
    assert process_payment("bank", 100.0, {"account": "123"}) == {"status": "ok", "fee": 0.8, "ref": "ach-123"}


def test_unknown_kind_raises():
    with pytest.raises(ValueError, match="unknown payment kind"):
        process_payment("cheque", 1.0, {})
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
