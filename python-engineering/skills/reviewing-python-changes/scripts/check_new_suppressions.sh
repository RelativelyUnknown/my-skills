#!/usr/bin/env bash
# Usage: check_new_suppressions.sh [revision-range]   (default: origin/main)
# Exits 1 when the diff adds a skip, xfail, ignore, noqa or blind except to Python files.
range="${1:-origin/main}"
if git diff "$range" -U0 -- '*.py' | grep -E '^\+[^+].*(pytest\.mark\.(skip|xfail)|type: ignore|noqa|except Exception|except:)'; then
  echo "New skip, xfail, ignore or blind except: needs human review." >&2
  exit 1
fi
