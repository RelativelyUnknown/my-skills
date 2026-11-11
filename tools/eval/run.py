#!/usr/bin/env python3
"""run.py: run eval cases in small batches and stop at the first usage-limit error.

    python3 tools/eval/run.py --out DIR [--cases a,b,c | --all | --errored] [--model claude-haiku-5-5]
        [--runs 3] [--ablation with-without] [--batch 3] [--plugin tabby] [--jobs 2] [--eval-dir DIR]

Each case writes DIR/<case>.json (and DIR/<case>/ for the report). A case whose JSON already exists with no errored run
is skipped, so a run can be resumed. After each case the JSON is read; if any run errored with a limit message the
driver stops launching new cases, prints which were not run, and exits 3. Nothing under the plugin folder is touched.
Needs the `claude` CLI; the eval CLI needs bubblewrap and socat for Bash graders.
"""
import argparse, json, os, subprocess, sys, concurrent.futures as cf

LIMIT = ("hit your", "limit", "resets")


def case_names(plugin_dir):
    d = os.path.join(plugin_dir, "evals")
    return sorted(n for n in os.listdir(d) if os.path.isfile(os.path.join(d, n, "case.yaml")))


def read(path):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return None


def errors_of(doc):
    out = []
    for c in (doc or {}).get("cases", []):
        for arm, runs in c.get("arms", {}).items():
            for r in runs:
                if r.get("error"):
                    out.append(str(r["error"]))
    return out


def is_limit(msgs):
    return any(all(w in m.lower() for w in LIMIT[:1]) and "limit" in m.lower() for m in msgs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cases", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--errored", action="store_true", help="only cases whose JSON in --out has an errored run")
    ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--judge-model", default="haiku")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--ablation", default="with-without")
    ap.add_argument("--batch", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--plugin", default=".", help="plugin name or path, as `claude plugin eval` takes it")
    ap.add_argument("--plugin-dir", default=".", help="folder holding evals/, to list cases")
    ap.add_argument("--max-cost-usd", default="5")
    ap.add_argument("--keep-temp", action="store_true", help="keep scaffold dirs so tracePath files survive (traces.py reads them)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    names = [c for c in a.cases.split(",") if c] or case_names(a.plugin_dir)
    todo = []
    for n in names:
        doc = read(os.path.join(a.out, n + ".json"))
        if doc is None:
            if not a.errored:
                todo.append(n)
        elif errors_of(doc):
            todo.append(n)
    print(f"{len(names)} cases considered, {len(todo)} to run, batch {a.batch}", flush=True)

    def one(n):
        cmd = ["claude", "plugin", "eval", a.plugin, "--case", n, "--runs", str(a.runs), "--ablation", a.ablation,
               "--scaffold", "--allow-tools", "Write", "Edit", "Bash", "WebFetch", "--model", a.model,
               "--judge-model", a.judge_model, "-j", str(a.jobs), "--max-cost-usd", a.max_cost_usd,
               "--trust-plugin", "--no-publish", "--json", os.path.join(a.out, n + ".json"),
               "--output-dir", os.path.join(a.out, n)]
        if a.keep_temp:
            cmd.append("--keep-temp")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        doc = read(os.path.join(a.out, n + ".json"))
        return n, doc

    stopped, done, notrun = False, 0, []
    for i in range(0, len(todo), a.batch):
        batch = todo[i:i + a.batch]
        if stopped:
            notrun += batch
            continue
        with cf.ThreadPoolExecutor(len(batch)) as ex:
            for n, doc in ex.map(one, batch):
                errs = errors_of(doc)
                done += 1
                tag = "LIMIT" if is_limit(errs) else ("errors:%d" % len(errs) if errs else "ok")
                print(f"  {n}: {tag}", flush=True)
                if is_limit(errs):
                    stopped = True
    if stopped:
        print("stopped at the first limit error. not run:", ",".join(notrun) or "(none)")
        sys.exit(3)
    print(f"finished {done} cases")


if __name__ == "__main__":
    main()
