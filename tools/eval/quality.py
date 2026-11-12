#!/usr/bin/env python3
"""quality.py: score the kept working directories of an eval run with hidden tests and static metrics.

    python3 tools/eval/quality.py RESULT_DIR [--cases a,b] [--csv out.csv]

RESULT_DIR holds <case>.json written by tools/eval/run.py with --keep-temp. For every run the agent's final working
directory (<trace dir>/../home/cwd) is copied to a scratch folder; evals/quality/hidden/<case>/test_hidden.py is added and
run with pytest (never present while the agent worked). Per run it reports the fraction of hidden tests that pass, whether
the whole project's own suite is green, ruff errors added, lines added and removed against the base commit, files touched,
new files, new dependencies, suppressions added (noqa, type: ignore, skip, xfail), plus the run's cost and turns.
No LLM judge. Needs pytest and ruff on PATH.
"""
import argparse, csv, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HIDDEN = os.path.join(HERE, "..", "..", "evals", "quality", "hidden")
TOTALS = {"bug-fix-starts-red": 8, "batches-and-utc": 6, "bounded-fan-out-with-deadline": 5,
          "dedupe-lines-script": 5, "import-rows-some-fail": 4, "tiny-fix-stays-tiny": 2}
SUPPRESS = re.compile(r"noqa|type:\s*ignore|pytest\.mark\.(skip|xfail)|@pytest\.mark\.skip|\.skip\(|xfail")


def sh(cmd, cwd, env=None, timeout=180):
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def passed_count(out):
    m = re.search(r"(\d+) passed", out)
    return int(m.group(1)) if m else 0


def score_dir(case, src):
    work = tempfile.mkdtemp(prefix="quality-")
    cwd = os.path.join(work, "cwd")
    shutil.copytree(src, cwd, symlinks=True)
    env = dict(os.environ, PYTHONPATH="src", PYTHONDONTWRITEBYTECODE="1")
    sh(["git", "add", "-A", "-N"], cwd)
    _, num = sh(["git", "diff", "--numstat", "HEAD", "--", ".", ":(exclude)*.lock"], cwd)
    added = removed = files = 0
    for line in num.splitlines():
        a, r, _name = (line.split("\t") + ["", "", ""])[:3]
        if a.isdigit():
            added += int(a); removed += int(r); files += 1
    _, st = sh(["git", "status", "--porcelain"], cwd)
    junk = re.compile(r"(__pycache__|\.pytest_cache|\.ruff_cache|\.hypothesis|\.mypy_cache|\.pyc$|\.db$)")
    new_files = sum(1 for l in st.splitlines() if l[:2] in ("??", "A ", " A", "AM") and not junk.search(l))
    _, diff = sh(["git", "diff", "HEAD", "-U0"], cwd)
    plus = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    suppress = sum(1 for l in plus if SUPPRESS.search(l))
    deps = 0
    in_deps = False
    for l in plus:
        if re.match(r"\s*dependencies\s*=", l) or re.match(r'\s*"[A-Za-z0-9_.\-\[\]]+[<>=!~ ]', l) and "pytest" not in l:
            deps += 1
    shutil.copy(os.path.join(HIDDEN, case, "test_hidden.py"), os.path.join(cwd, "test_hidden.py"))
    rc, out = sh(["pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "test_hidden.py"], cwd, env)
    hidden = passed_count(out) / TOTALS[case]
    os.remove(os.path.join(cwd, "test_hidden.py"))
    rc2, out2 = sh(["pytest", "-q", "-p", "no:cacheprovider", "--tb=no"], cwd, env)
    suite_green = rc2 == 0 or "no tests ran" in out2
    def ruff_count(path):
        _, o = sh(["ruff", "check", "--select", "E,F,B,UP", "--output-format", "concise", "--no-cache", "."], path)
        return len([l for l in o.splitlines() if re.match(r".+:\d+:\d+:", l)])

    base = os.path.join(work, "base")
    os.makedirs(base)
    p1 = subprocess.run(["git", "archive", "HEAD"], cwd=cwd, capture_output=True)
    subprocess.run(["tar", "-x", "-C", base], input=p1.stdout, capture_output=True)
    ruff_errs = max(0, ruff_count(cwd) - ruff_count(base))
    shutil.rmtree(work, ignore_errors=True)
    return dict(hidden=round(hidden, 3), suite_green=int(suite_green), ruff=ruff_errs, added=added, removed=removed,
                files=files, new_files=new_files, suppressions=suppress, dep_lines=deps)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result_dir")
    ap.add_argument("--cases", default="")
    ap.add_argument("--csv", default="")
    a = ap.parse_args()
    names = [c for c in a.cases.split(",") if c] or sorted(TOTALS)
    rows = []
    for case in names:
        path = os.path.join(a.result_dir, case + ".json")
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        doc = json.load(open(path))["cases"][0]
        for arm, runs in doc["arms"].items():
            for i, r in enumerate(runs):
                tp = r.get("tracePath") or ""
                src = os.path.join(os.path.dirname(os.path.dirname(tp)), "home", "cwd")
                if not os.path.isdir(src):
                    print("no kept dir for", case, arm, i + 1, file=sys.stderr)
                    continue
                m = score_dir(case, src)
                m.update(case=case, arm=arm, run=i + 1, cost=round(r["costUsd"], 4), turns=r["turns"], error=bool(r["error"]))
                rows.append(m)
                print(json.dumps(m), flush=True)
    if a.csv and rows:
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
    # per-arm means
    arms = sorted({r["arm"] for r in rows})
    keys = ["hidden", "suite_green", "ruff", "added", "removed", "files", "new_files", "suppressions", "dep_lines", "cost", "turns"]
    print("\narm    n  " + "  ".join(f"{k:>11}" for k in keys))
    for arm in arms:
        rs = [r for r in rows if r["arm"] == arm]
        print(f"{arm:6} {len(rs):<2} " + "  ".join(f"{sum(r[k] for r in rs)/len(rs):11.3f}" for k in keys))


if __name__ == "__main__":
    main()
