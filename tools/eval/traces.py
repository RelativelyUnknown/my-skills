#!/usr/bin/env python3
"""traces.py: summarise what an agent did in a kept eval trace (`--keep-temp`).

    python3 tools/eval/traces.py TRACE.jsonl [TRACE2.jsonl ...] [--json]

Per trace: number of assistant turns, the skill files read (paths containing /tabby/ or /skills/), total bytes of those
reads when the file can be found, the turn of the first Write or Edit, Bash commands that mention a checker, and the
ordered tool list. Reads the `assistant` messages' tool_use blocks.
"""
import json, sys, os, re


def events(path):
    for ln in open(path, errors="ignore"):
        try:
            yield json.loads(ln)
        except ValueError:
            continue


def summarise(path):
    turn_of, tools, reads, first_edit, checks = {}, [], [], None, []
    seen_tools = set()
    for e in events(path):
        if e.get("type") != "assistant":
            continue
        msg = e.get("message", {})
        mid = msg.get("id")
        if mid not in turn_of:
            turn_of[mid] = len(turn_of) + 1
        turn = turn_of[mid]
        for b in msg.get("content", []):
            if b.get("type") != "tool_use" or b.get("id") in seen_tools:
                continue
            seen_tools.add(b.get("id"))
            name, inp = b.get("name"), b.get("input", {})
            tools.append((turn, name, inp))
            if name == "Read":
                reads.append((turn, inp.get("file_path", "")))
            if name in ("Write", "Edit") and first_edit is None:
                first_edit = turn
            if name == "Bash" and re.search(r"check\.py|check-motion|ui-check|make\.mjs|animate\.mjs|pytest|ruff|mypy", inp.get("command", "")):
                checks.append((turn, inp["command"][:90]))
    turn = len(turn_of)
    skill_reads = [(t, p) for t, p in reads if re.search(r"/(tabby|skills)/", p) and p.endswith(".md")]
    return dict(trace=path, turns=turn, tool_calls=len(tools), skill_reads=skill_reads, first_edit_turn=first_edit,
                checks=checks, order=[n for _, n, _ in tools])


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__); return 1
    out = [summarise(f) for f in files]
    if as_json:
        print(json.dumps(out, indent=1)); return 0
    for s in out:
        print(f"{s['trace']}: {s['turns']} turns, {s['tool_calls']} tool calls, first Write/Edit at turn {s['first_edit_turn']}")
        print(f"  skill files read ({len(s['skill_reads'])}):")
        for t, p in s["skill_reads"]:
            print(f"    turn {t:>2}  {p.split('/tabby/')[-1]}")
        for t, c in s["checks"]:
            print(f"  turn {t:>2}  ran: {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
