#!/usr/bin/env bash
set -euo pipefail
git init -q -b main
touch .gitkeep
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
