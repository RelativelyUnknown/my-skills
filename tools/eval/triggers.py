#!/usr/bin/env python3
"""triggers.py: which Tabby skill does a prompt load? Writes a per-query result and a confusion matrix.

    python3 tools/eval/triggers.py --out results.json [--queries evals/triggers.skills.json] [--runs 3] [--model claude-haiku-5-5]
        [--plugin-dir .] [--turns 4] [--jobs 6]

Each query is run with `claude -p` in an empty scratch folder with the plugin loaded; the skill chosen is the first `Skill` tool call
(or `none` when the run ends, or edits a file, before any). A query's `expect` is a skill name, a list of acceptable names, or `none`.
"""
import argparse, json, os, subprocess, tempfile, collections, concurrent.futures as cf


def first_skill(events):
    for e in events:
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    if c["name"] == "Skill":
                        return str(c["input"].get("skill", "?")).split(":")[-1]
                    if c["name"] in ("Write", "Edit"):
                        return "none"
    return "none"


def run(q, a):
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run(["claude", "-p", q, "--plugin-dir", a.plugin_dir, "--model", a.model, "--max-turns", str(a.turns),
                            "--output-format", "stream-json", "--verbose"] + (["--settings", a.settings] if a.settings else []), cwd=d, capture_output=True, text=True)
    ev = []
    for l in p.stdout.splitlines():
        try:
            ev.append(json.loads(l))
        except ValueError:
            pass
    cost = next((e.get("total_cost_usd", 0) for e in ev if e.get("type") == "result"), 0)
    return first_skill(ev), cost


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--queries", default="evals/triggers.skills.json")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--plugin-dir", default=".")
    ap.add_argument("--turns", type=int, default=4)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--settings", default="", help="a settings.json to pass to claude (for example one with a UserPromptSubmit hook)")
    a = ap.parse_args()
    a.plugin_dir = os.path.abspath(a.plugin_dir)
    qs = json.load(open(a.queries))
    jobs = [(i, r) for i in range(len(qs)) for r in range(a.runs)]
    res = collections.defaultdict(list)
    cost = 0
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for (i, r), (sk, c) in zip(jobs, ex.map(lambda j: run(qs[j[0]]["query"], a), jobs)):
            res[i].append(sk)
            cost += c
    out, ok, total = [], 0, 0
    conf = collections.Counter()
    for i, q in enumerate(qs):
        exp = q["expect"] if isinstance(q["expect"], list) else [q["expect"]]
        hits = sum(s in exp for s in res[i])
        ok += hits
        total += len(res[i])
        for s in res[i]:
            conf[(exp[0], s)] += 1
        out.append({"query": q["query"], "expect": q["expect"], "got": res[i], "correct": hits})
    json.dump({"model": a.model, "runs": a.runs, "cost_usd": cost, "correct": ok, "total": total, "results": out}, open(a.out, "w"), indent=1)
    print(f"{ok}/{total} correct, cost ${cost:.2f}")
    names = sorted({k[0] for k in conf} | {k[1] for k in conf})
    print("rows = expected, columns = loaded")
    print("%-16s" % "" + "".join("%-14s" % n for n in names))
    for e in names:
        print("%-16s" % e + "".join("%-14d" % conf[(e, g)] for g in names))
    for o in out:
        if o["correct"] < len(o["got"]):
            print("MISS", o["correct"], "/", len(o["got"]), o["expect"], o["got"], o["query"])


main()
