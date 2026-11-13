#!/usr/bin/env bash
# Builds the fixture project for the `real-own-code-stubbed-edge` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
package = true

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/__init__.py)"
cat > src/shop/__init__.py <<'__FIXTURE_EOF__'
from shop.gateway import PaymentError, PaymentGateway
from shop.inventory import Inventory, OutOfStock
from shop.orders import place_order

__all__ = ["Inventory", "OutOfStock", "PaymentError", "PaymentGateway", "place_order"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/inventory.py)"
cat > src/shop/inventory.py <<'__FIXTURE_EOF__'
class OutOfStock(Exception):
    pass


class Inventory:
    """In-memory stock levels. Reserving removes units; releasing puts them back."""

    def __init__(self, stock: dict[str, int]) -> None:
        self._stock = dict(stock)

    def available(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def reserve(self, sku: str, quantity: int) -> None:
        if self.available(sku) < quantity:
            raise OutOfStock(f"{sku!r}: wanted {quantity}, have {self.available(sku)}")
        self._stock[sku] -= quantity

    def release(self, sku: str, quantity: int) -> None:
        self._stock[sku] = self.available(sku) + quantity
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/gateway.py)"
cat > src/shop/gateway.py <<'__FIXTURE_EOF__'
import json
import urllib.error
import urllib.request


class PaymentError(Exception):
    pass


class PaymentGateway:
    """Client for the payment provider's HTTP API."""

    def __init__(self, base_url: str, token: str, *, timeout: float = 5) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._timeout = timeout

    def charge(self, amount_cents: int, card_token: str) -> str:
        """Charge the card and return the provider's charge id."""
        body = json.dumps({"amount": amount_cents, "card": card_token}).encode()
        request = urllib.request.Request(
            f"{self._base_url}/charges",
            data=body,
            headers={"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                return json.load(response)["id"]
        except (urllib.error.URLError, TimeoutError) as error:
            raise PaymentError(f"charge of {amount_cents} cents failed") from error
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/orders.py)"
cat > src/shop/orders.py <<'__FIXTURE_EOF__'
from shop.gateway import PaymentGateway
from shop.inventory import Inventory


def place_order(
    inventory: Inventory,
    gateway: PaymentGateway,
    sku: str,
    quantity: int,
    unit_price_cents: int,
    card_token: str,
) -> str:
    """Reserve stock, charge the card and return the charge id. A failed charge puts the stock back."""
    inventory.reserve(sku, quantity)
    try:
        return gateway.charge(quantity * unit_price_cents, card_token)
    except Exception:
        inventory.release(sku, quantity)
        raise
__FIXTURE_EOF__
mkdir -p "$(dirname tests/.gitkeep)"
cat > tests/.gitkeep <<'__FIXTURE_EOF__'

__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
