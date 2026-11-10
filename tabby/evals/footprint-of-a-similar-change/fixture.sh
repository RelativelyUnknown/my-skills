#!/usr/bin/env bash
# Builds the fixture project for the `footprint-of-a-similar-change` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "inventory"
version = "1.1.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
inventory = "inventory.cli:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
mkdir -p "$(dirname src/inventory/__init__.py)"
cat > src/inventory/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/inventory/cli.py)"
cat > src/inventory/cli.py <<'__FIXTURE_EOF__'
import argparse
import sys


ITEMS = [("bolt", 40), ("nut", 25), ("washer", 0)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inventory")
    args = parser.parse_args(argv)
    for name, count in ITEMS:
        print(f"{name}\t{count}")
    print(f"{len(ITEMS)} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_cli.py)"
cat > tests/test_cli.py <<'__FIXTURE_EOF__'
from inventory.cli import main


def test_lists_items(capsys):
    main([])
    assert "bolt" in capsys.readouterr().out
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# inventory

Lists stock levels.

## Usage

    inventory
__FIXTURE_EOF__
mkdir -p "$(dirname CHANGELOG.md)"
cat > CHANGELOG.md <<'__FIXTURE_EOF__'
# Changelog

## [1.1.0] - 2026-09-01
### Added
- First release.
__FIXTURE_EOF__
mkdir -p "$(dirname completions/inventory.bash)"
cat > completions/inventory.bash <<'__FIXTURE_EOF__'
_inventory() {
    COMPREPLY=( $(compgen -W "--help" -- "${COMP_WORDS[COMP_CWORD]}") )
}
complete -F _inventory inventory
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
git config user.email eval@example.com; git config user.name eval
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "inventory"
version = "1.2.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
inventory = "inventory.cli:main"

[tool.pytest.ini_options]
pythonpath = ["src"]
__FIXTURE_EOF__
cat > src/inventory/cli.py <<'__FIXTURE_EOF__'
import argparse
import sys


ITEMS = [("bolt", 40), ("nut", 25), ("washer", 0)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="inventory")
    parser.add_argument("--min", type=int, default=0, help="hide items below this stock level")
    args = parser.parse_args(argv)
    shown = [(name, n) for name, n in ITEMS if n >= args.min]
    for name, count in shown:
        print(f"{name}\t{count}")
    print(f"{len(shown)} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
__FIXTURE_EOF__
cat > tests/test_cli.py <<'__FIXTURE_EOF__'
from inventory.cli import main


def test_lists_items(capsys):
    main([])
    assert "bolt" in capsys.readouterr().out


def test_min(capsys):
    main(["--min", "30"])
    assert "nut" not in capsys.readouterr().out
__FIXTURE_EOF__
cat > README.md <<'__FIXTURE_EOF__'
# inventory

Lists stock levels.

## Usage

    inventory [--min N]

`--min N` hides items with fewer than N in stock.
__FIXTURE_EOF__
cat > CHANGELOG.md <<'__FIXTURE_EOF__'
# Changelog

## [1.2.0] - 2026-10-01
### Added
- `--min N` hides items below a stock level.

## [1.1.0] - 2026-09-01
### Added
- First release.
__FIXTURE_EOF__
cat > completions/inventory.bash <<'__FIXTURE_EOF__'
_inventory() {
    COMPREPLY=( $(compgen -W "--min --help" -- "${COMP_WORDS[COMP_CWORD]}") )
}
complete -F _inventory inventory
__FIXTURE_EOF__
git add -A; git commit -qm "Add --min flag: cli, test, README, changelog, completion"
