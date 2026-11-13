#!/usr/bin/env python3
"""install.py: copy the Tabby skills to where OpenCode, GitHub Copilot or Claude Code read them.

    python3 tools/install.py TARGET [--user] [--dest DIR] [--force] [--dry-run] [--with-hooks]

TARGET picks the skills folder (project scope is relative to the current directory; --user uses your home folder):

    agents    .agents/skills        ~/.agents/skills         OpenCode and Copilot read it (Claude Code does not)
    claude    .claude/skills        ~/.claude/skills         Claude Code, OpenCode and Copilot read it
    github    .github/skills        ~/.copilot/skills        Copilot
    opencode  .opencode/skills      ~/.config/opencode/skills  OpenCode

Claude Code users can install the plugin instead (see the README). Without --force an existing skill folder is left
alone and reported; with --force files are overwritten in place and nothing is deleted. The `hooks` skill is Claude Code
only and is copied only with --with-hooks. Stdlib only.
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILLS = ["tabby", "tabby-review", "tabby-docs", "tabby-diagrams", "tabby-frontend", "interview"]
WHERE = {
    "agents": (".agents/skills", "~/.agents/skills"),
    "claude": (".claude/skills", "~/.claude/skills"),
    "github": (".github/skills", "~/.copilot/skills"),
    "opencode": (".opencode/skills", "~/.config/opencode/skills"),
}
NEXT = {
    "agents": "OpenCode: ask for the skill by name or write @tabby. Copilot: type /tabby in chat.",
    "claude": "Claude Code loads the skills on its own; OpenCode and Copilot read this folder too.",
    "github": "Copilot loads a skill when your request matches it, or type /tabby in chat.",
    "opencode": "OpenCode lists the skills to the model; write @tabby to load one by name.",
}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Copy the Tabby skills to a harness's skills folder.")
    ap.add_argument("target", choices=sorted(WHERE))
    ap.add_argument("--user", action="store_true", help="install for your user, not the current project")
    ap.add_argument("--dest", help="skills folder to use instead of the default for TARGET")
    ap.add_argument("--force", action="store_true", help="overwrite files in skill folders that already exist")
    ap.add_argument("--dry-run", action="store_true", help="show what would be copied and change nothing")
    ap.add_argument("--with-hooks", action="store_true", help="also copy the Claude Code only hooks skill")
    a = ap.parse_args(argv)

    dest = a.dest or WHERE[a.target][1 if a.user else 0]
    dest = os.path.abspath(os.path.expanduser(dest))
    names = SKILLS + (["hooks"] if a.with_hooks else [])
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
    done, skipped = [], []
    for name in names:
        src = os.path.join(ROOT, name)
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            print(f"missing {src}/SKILL.md; run this from a full copy of the repository", file=sys.stderr)
            return 2
        out = os.path.join(dest, name)
        if os.path.exists(out) and not a.force:
            skipped.append(name)
            continue
        if not a.dry_run:
            os.makedirs(dest, exist_ok=True)
            shutil.copytree(src, out, ignore=ignore, dirs_exist_ok=True)
        done.append(name)
    verb = "would copy" if a.dry_run else "copied"
    print(f"{verb} {len(done)} skill(s) to {dest}: {', '.join(done) or 'none'}")
    if skipped:
        print(f"left alone (already there; use --force to overwrite files): {', '.join(skipped)}")
    if done and not a.dry_run:
        print(NEXT[a.target])
        print("The skills point at each other by relative path, so keep the folders side by side.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
