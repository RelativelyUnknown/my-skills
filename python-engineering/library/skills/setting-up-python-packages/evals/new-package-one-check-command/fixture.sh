#!/usr/bin/env bash
# Builds the fixture project for the `new-package-one-check-command` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# ledgerlib

Planned library. Nothing here yet.
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
