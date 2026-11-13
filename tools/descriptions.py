#!/usr/bin/env python3
"""descriptions.py: every SKILL.md description must be at most 1,024 characters (the plugin limit).

    python3 tools/descriptions.py        exits 1 and names each skill over the limit
"""
import glob
import re
import sys

LIMIT = 1024
bad = 0
for path in sorted(glob.glob("**/SKILL.md", recursive=True)):
    text = open(path, errors="ignore").read()
    m = re.search(r'^description:\s*"(.*)"\s*$', text, re.M) or re.search(r"^description:\s*(.+)$", text, re.M)
    if not m:
        print(f"{path}: no description")
        bad += 1
        continue
    n = len(m.group(1))
    print(f"{path}: {n}" + ("  OVER" if n > LIMIT else ""))
    bad += n > LIMIT
sys.exit(1 if bad else 0)
