#!/usr/bin/env python3
"""judge.py: blind, order-swapped paired judging of the code an agent left behind.

    python3 tools/eval/judge.py RESULT_DIR [--cases a,b] [--judge-model claude-sonnet-5-5] [--jobs 6] [--out judged.json]

RESULT_DIR holds <case>.json written by tools/eval/run.py with --keep-temp and both arms (default ablation). For each case
and run index it takes the with-skill and without-skill final working directories, builds each one's diff against its base
commit, and asks a judge model which solution a senior reviewer would rather merge. Every pair is judged twice with A and B
swapped. The prompt never names the skill, the arm or Tabby; the rubric is plain language drawn from common code-quality
catalogs and tabby/development/architecture/senior-engineering.md.

Reported: wins, losses and ties for the with-skill arm over the pairs where both orderings agree, how many pairs the two
orderings disagreed on (order bias), and mean 1 to 5 scores per criterion. Disagreeing pairs count as ties. Needs `claude`
on PATH. Costs roughly two judge calls per pair.
"""
import argparse
import collections
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "..", "..", "evals")
MAX_DIFF = 14000
CRITERIA = ["solves_the_real_problem", "minimal_and_fits_the_codebase", "errors_and_invariants", "reuses_what_exists",
            "flat_control_flow", "abstraction_earns_its_coupling", "readable_and_honest_comments",
            "tests_that_would_catch_a_regression"]

RUBRIC = """You are a senior engineer reviewing two candidate changes (A and B) for the same task. Decide which one you would rather merge.

Judge the code, not the explanation. Criteria, each scored 1 (poor) to 5 (excellent) for both candidates. If a criterion does not apply to this task, score both 3:
- solves_the_real_problem: fixes the cause, not the symptom; no special-casing of inputs, no hiding the failure.
- minimal_and_fits_the_codebase: as small as it can be while correct; follows the style and structure already there; no speculative generality, no unrequested features or layers.
- errors_and_invariants: errors are handled where they can be acted on, not swallowed; what must be true is checked, not only commented; no defensive checks on data the code itself produced.
- reuses_what_exists: uses the standard library or an existing helper instead of reimplementing it.
- flat_control_flow: no more than three levels of nesting; the unhappy path is handled early (guard clauses) and the main logic stays at the top level; long blocks are split into well-named functions with one job each.
- abstraction_earns_its_coupling: every base class, interface or flag is justified by three or more variants or by deferred or repeated use; a new variant lives beside the old one instead of branching through it; a little repetition is preferred to coupling unrelated code.
- readable_and_honest_comments: clear names; magic numbers are named; a comment explaining a complex condition is replaced by a named variable or function; comments explain why, not what; no commented-out code; no filler.
- tests_that_would_catch_a_regression: tests fail without the change and assert real behaviour; none were weakened or skipped. If the task needed no tests, score both 3.

Do not prefer a candidate for being longer, for having more comments or tests, or for sounding more careful. A smaller correct change beats a larger one.

Reply with only a JSON object: {"winner": "A" | "B" | "tie", "scores": {"A": {criterion: n, ...}, "B": {criterion: n, ...}}, "reason": "one sentence"}."""


def sh(cmd, cwd=None, inp=None, timeout=300):
    try:
        p = subprocess.run(cmd, cwd=cwd, input=inp, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, ""


def diff_of(src):
    work = tempfile.mkdtemp(prefix="judge-")
    try:
        dst = os.path.join(work, "d")
        shutil.copytree(src, dst, symlinks=True)
        sh(["git", "add", "-A", "-N"], dst)
        _, d = sh(["git", "diff", "HEAD", "--", ".", ":(exclude)*.lock", ":(exclude)*.pyc", ":(exclude)__pycache__",
                   ":(exclude).pytest_cache", ":(exclude).ruff_cache"], dst)
        return d[:MAX_DIFF] + ("\n[diff cut]" if len(d) > MAX_DIFF else "")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run_dir(run):
    tp = run.get("tracePath") or ""
    d = os.path.join(os.path.dirname(os.path.dirname(tp)), "home", "cwd")
    return d if os.path.isdir(d) else None


def task_of(case):
    p = os.path.join(CASES, case, "prompt.md")
    t = open(p).read() if os.path.exists(p) else ""
    return re.sub(r"\A---.*?---\s*", "", t, flags=re.S).strip()


def ask(model, task, first, second):
    body = f"{RUBRIC}\n\n# Task\n{task}\n\n# Candidate A (diff)\n{first}\n\n# Candidate B (diff)\n{second}\n"
    with tempfile.TemporaryDirectory() as d:
        rc, out = sh(["claude", "-p", body, "--model", model, "--max-turns", "1", "--output-format", "text"], cwd=d)
    m = re.search(r"\{.*\}", out, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except ValueError:
        return None


def judge_pair(args):
    case, i, model, task, d_with, d_without = args
    r1 = ask(model, task, d_with, d_without)      # with = A
    r2 = ask(model, task, d_without, d_with)      # with = B
    return case, i, r1, r2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result_dir")
    ap.add_argument("--cases", default="")
    ap.add_argument("--judge-model", default="claude-sonnet-5-5")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    names = [c for c in a.cases.split(",") if c] or sorted(f[:-5] for f in os.listdir(a.result_dir) if f.endswith(".json"))
    jobs = []
    for case in names:
        path = os.path.join(a.result_dir, case + ".json")
        if not os.path.exists(path):
            continue
        arms = json.load(open(path))["cases"][0]["arms"]
        if "with" not in arms or "without" not in arms:
            print("skip", case, "(needs both arms)", file=sys.stderr)
            continue
        task = task_of(case)
        for i, (rw, ro) in enumerate(zip(arms["with"], arms["without"])):
            dw, do = run_dir(rw), run_dir(ro)
            if dw and do:
                jobs.append((case, i + 1, a.judge_model, task, diff_of(dw), diff_of(do)))
    print(f"{len(jobs)} pairs, {2 * len(jobs)} judge calls", file=sys.stderr)
    rows, win, loss, tie, split, bad = [], 0, 0, 0, 0, 0
    crit = collections.defaultdict(lambda: [0, 0, 0])   # sum with, sum without, n
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for case, i, r1, r2 in ex.map(judge_pair, jobs):
            if not r1 or not r2:
                bad += 1
                continue
            v1 = {"A": "with", "B": "without", "tie": "tie"}.get(r1.get("winner"), "tie")
            v2 = {"A": "without", "B": "with", "tie": "tie"}.get(r2.get("winner"), "tie")
            if v1 == v2:
                verdict = v1
            else:
                verdict = "split"
            win += verdict == "with"
            loss += verdict == "without"
            tie += verdict == "tie"
            split += verdict == "split"
            for c in CRITERIA:
                try:
                    crit[c][0] += (r1["scores"]["A"][c] + r2["scores"]["B"][c]) / 2
                    crit[c][1] += (r1["scores"]["B"][c] + r2["scores"]["A"][c]) / 2
                    crit[c][2] += 1
                except (KeyError, TypeError):
                    pass
            rows.append(dict(case=case, run=i, verdict=verdict, first=r1.get("reason"), second=r2.get("reason")))
    n = win + loss + tie + split
    print(f"\npairs judged: {n} (unparseable: {bad}); judge {a.judge_model}")
    print(f"with-skill wins {win}, loses {loss}, ties {tie}, orderings disagreed {split}")
    print("\ncriterion                              with   without")
    for c in CRITERIA:
        s, o, k = crit[c]
        if k:
            print(f"{c:36} {s / k:6.2f} {o / k:8.2f}")
    if a.out:
        json.dump(dict(rows=rows, win=win, loss=loss, tie=tie, split=split), open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
