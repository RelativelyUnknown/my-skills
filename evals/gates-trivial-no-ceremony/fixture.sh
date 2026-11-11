#!/usr/bin/env bash
# Builds the fixture project for the `gates-trivial-no-ceremony` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# notifier

The service will recieve events and forward them.
__FIXTURE_EOF__
mkdir -p "$(dirname src/notifier/__init__.py)"
cat > src/notifier/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
