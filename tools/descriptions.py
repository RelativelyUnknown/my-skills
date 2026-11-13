#!/usr/bin/env python3
"""descriptions.py: check every SKILL.md against the Agent Skills standard that Claude Code, OpenCode and Copilot share.

    python3 tools/descriptions.py        exits 1 and names each problem

Checks: `name` is 1 to 64 lowercase letters, digits and single hyphens and equals the folder name; `description` is
present and at most 1,024 characters; the file is at most 500 lines (the standard's advice for progressive disclosure).
`allowed-tools` is optional and not checked. Run from the repository root.
"""
import glob
import os
import re
import sys

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
bad = 0


def field(text, key):
    m = re.search(rf'^{key}:\s*"(.*)"\s*$', text, re.M) or re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


for path in sorted(glob.glob("**/SKILL.md", recursive=True)):
    text = open(path, errors="ignore").read()
    folder = os.path.basename(os.path.dirname(path)) or "."
    name, desc = field(text, "name"), field(text, "description")
    problems = []
    if not name or not NAME.match(name) or len(name) > 64:
        problems.append(f"name {name!r} is not 1 to 64 lowercase letters, digits and single hyphens")
    elif name != folder:
        problems.append(f"name {name!r} does not match the folder {folder!r}")
    if not desc:
        problems.append("no description")
    elif len(desc) > 1024:
        problems.append(f"description is {len(desc)} characters (limit 1,024)")
    lines = text.count("\n") + 1
    if lines > 500:
        problems.append(f"{lines} lines (advice: at most 500)")
    print(f"{path}: {len(desc or '')} chars, {lines} lines" + ("  " + "; ".join(problems) if problems else ""))
    bad += bool(problems)
sys.exit(1 if bad else 0)
