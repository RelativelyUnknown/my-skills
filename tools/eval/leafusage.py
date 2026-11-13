#!/usr/bin/env python3
"""leafusage.py: which content files do eval agents actually open?

    python3 tools/eval/leafusage.py [--traces 'GLOB'] [--top 20] [--json]

Reads kept traces (`run.py --keep-temp`; default glob /tmp/claude-eval-*/out/trace.jsonl) and counts, per content
file under tabby*/ and interview/, the traces that Read it. A path counts when it contains /plugin/ (the copy the
runner passes) or starts at the repository root. SKILL.md files are loaded through the Skill tool, not Read, so they
are listed apart. Run from the repository root.

A file never read is not proof it is useless: the cases may not exercise it. It does show where an ablation cannot
show a difference, so do not prune on this alone.
"""
import argparse
import collections
import glob
import json
import re
import sys


def traces_reads(pattern):
    n = 0
    counts = collections.Counter()
    for t in glob.glob(pattern):
        try:
            msgs = [json.loads(line) for line in open(t) if line.strip()]
        except (OSError, ValueError):
            continue
        n += 1
        seen = set()
        for m in msgs:
            if m.get("type") != "assistant":
                continue
            for b in m["message"]["content"]:
                if b.get("type") == "tool_use" and b["name"] == "Read":
                    hit = re.search(r"/plugin/(.*)", b["input"].get("file_path", ""))
                    if hit:
                        seen.add(hit.group(1))
        counts.update(seen)
    return n, counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--traces", default="/tmp/claude-eval-*/out/trace.jsonl")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    n, counts = traces_reads(a.traces)
    files = [f for pat in ("tabby*/**/*.md", "interview/**/*.md") for f in glob.glob(pat, recursive=True)
             if not f.endswith(("SKILL.md", "SOURCE.md", "README.md"))]
    words = {f: len(open(f).read().split()) for f in files}
    unread = sorted((f for f in files if counts[f] == 0), key=lambda f: -words[f])
    out = {"traces": n, "files": len(files), "never_read": len(unread),
           "words_never_read": sum(words[f] for f in unread), "words_total": sum(words.values()),
           "never_read_largest": [[f, words[f]] for f in unread[:a.top]],
           "most_read": [[f, c] for f, c in counts.most_common(a.top) if f in words]}
    if a.json:
        json.dump(out, sys.stdout, indent=1)
        return
    print(f"{n} traces; {out['never_read']} of {out['files']} files never read "
          f"({out['words_never_read']} of {out['words_total']} words)")
    print("\nnever read, largest:")
    for f, w in out["never_read_largest"]:
        print(f"{w:6} {f}")
    print("\nmost read:")
    for f, c in out["most_read"]:
        print(f"{c:6} {f}")


if __name__ == "__main__":
    main()
