#!/usr/bin/env bash
# Builds the fixture project for the `vague-request-larger-repo` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "exporter"
version = "2.1.0"
requires-python = ">=3.12"

[project.scripts]
exporter = "exporter.cli:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# exporter

Writes the customer list as CSV or JSON for the finance team.

    exporter customers.db --format csv --out customers.csv
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/__init__.py)"
cat > src/exporter/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/cli.py)"
cat > src/exporter/cli.py <<'__FIXTURE_EOF__'
"""Command line entry point."""
import argparse
import sys
from pathlib import Path

from exporter import export, store


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("--format", choices=sorted(export.WRITERS), default="csv")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        customers = store.load_customers(args.database)
    except FileNotFoundError:
        print(f"no such database: {args.database}", file=sys.stderr)
        return 1
    args.out.write_text(export.render(customers, args.format), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/customers.py)"
cat > src/exporter/customers.py <<'__FIXTURE_EOF__'
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Customer:
    id: int
    name: str
    country: str
    balance: Decimal
    joined: date
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/store.py)"
cat > src/exporter/store.py <<'__FIXTURE_EOF__'
import sqlite3
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from exporter.customers import Customer


def load_customers(path: Path) -> list[Customer]:
    if not path.exists():
        raise FileNotFoundError(path)
    with closing(sqlite3.connect(path)) as conn:
        rows = conn.execute("SELECT id, name, country, balance, joined FROM customers ORDER BY id").fetchall()
    return [Customer(r[0], r[1], r[2], Decimal(r[3]), date.fromisoformat(r[4])) for r in rows]
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/money.py)"
cat > src/exporter/money.py <<'__FIXTURE_EOF__'
from decimal import ROUND_HALF_UP, Decimal


def format_amount(amount: Decimal) -> str:
    return str(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/dates.py)"
cat > src/exporter/dates.py <<'__FIXTURE_EOF__'
from datetime import date


def format_date(value: date) -> str:
    return value.isoformat()
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/countries.py)"
cat > src/exporter/countries.py <<'__FIXTURE_EOF__'
NAMES = {"DE": "Germany", "FR": "France", "NL": "Netherlands", "US": "United States"}


def country_name(code: str) -> str:
    if code not in NAMES:
        raise ValueError(f"unknown country code {code!r}; expected one of {sorted(NAMES)}")
    return NAMES[code]
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/export.py)"
cat > src/exporter/export.py <<'__FIXTURE_EOF__'
from collections.abc import Callable, Sequence

from exporter.customers import Customer
from exporter.formats import csv_format, json_format

WRITERS: dict[str, Callable[[Sequence[Customer]], str]] = {
    "csv": csv_format.write,
    "json": json_format.write,
}


def render(customers: Sequence[Customer], fmt: str) -> str:
    if fmt not in WRITERS:
        raise ValueError(f"unknown format {fmt!r}; expected one of {sorted(WRITERS)}")
    return WRITERS[fmt](customers)
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/formats/__init__.py)"
cat > src/exporter/formats/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/formats/json_format.py)"
cat > src/exporter/formats/json_format.py <<'__FIXTURE_EOF__'
import json
from collections.abc import Sequence

from exporter.countries import country_name
from exporter.customers import Customer
from exporter.dates import format_date
from exporter.money import format_amount


def write(customers: Sequence[Customer]) -> str:
    return json.dumps(
        [
            {
                "id": c.id,
                "name": c.name,
                "country": country_name(c.country),
                "balance": format_amount(c.balance),
                "joined": format_date(c.joined),
            }
            for c in customers
        ],
        ensure_ascii=False,
        indent=2,
    )
__FIXTURE_EOF__
mkdir -p "$(dirname src/exporter/formats/csv_format.py)"
cat > src/exporter/formats/csv_format.py <<'__FIXTURE_EOF__'
from collections.abc import Sequence

from exporter.countries import country_name
from exporter.customers import Customer
from exporter.dates import format_date
from exporter.money import format_amount

HEADER = ["id", "name", "country", "balance", "joined"]


def write(customers: Sequence[Customer]) -> str:
    lines = [",".join(HEADER)]
    for c in customers:
        fields = [str(c.id), c.name, country_name(c.country), format_amount(c.balance), format_date(c.joined)]
        lines.append(",".join(fields))
    return "\n".join(lines) + "\n"
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_csv_format.py)"
cat > tests/test_csv_format.py <<'__FIXTURE_EOF__'
from datetime import date
from decimal import Decimal

from exporter.customers import Customer
from exporter.formats import csv_format


def test_writes_header_and_rows():
    customers = [Customer(1, "Zoë Müller", "DE", Decimal("10.5"), date(2026, 1, 2))]
    assert csv_format.write(customers) == "id,name,country,balance,joined\n1,Zoë Müller,Germany,10.50,2026-01-02\n"
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_money.py)"
cat > tests/test_money.py <<'__FIXTURE_EOF__'
from decimal import Decimal

from exporter.money import format_amount


def test_rounds_half_up():
    assert format_amount(Decimal("1.005")) == "1.01"
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
