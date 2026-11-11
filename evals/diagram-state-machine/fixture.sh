#!/usr/bin/env bash
# Builds the fixture project for the `diagram-state-machine` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# shop

A small order service.
__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/__init__.py)"
cat > src/shop/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/shop/orders.py)"
cat > src/shop/orders.py <<'__FIXTURE_EOF__'
"""Order lifecycle."""
from enum import Enum


class OrderState(Enum):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


TRANSITIONS = {
    OrderState.CREATED: {OrderState.PAID, OrderState.CANCELLED},
    OrderState.PAID: {OrderState.SHIPPED, OrderState.CANCELLED},
    OrderState.SHIPPED: {OrderState.DELIVERED},
    OrderState.DELIVERED: set(),
    OrderState.CANCELLED: set(),
}


def move(current: OrderState, target: OrderState) -> OrderState:
    if target not in TRANSITIONS[current]:
        raise ValueError(f"cannot go from {current.value} to {target.value}")
    return target
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
