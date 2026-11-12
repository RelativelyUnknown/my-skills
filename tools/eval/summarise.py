#!/usr/bin/env python3
"""summarise.py: paired tables from `claude plugin eval --json` result files.

    python3 tools/eval/summarise.py DIR [--csv out.csv] [--compare OTHER_DIR]

DIR holds <case>.json files (as written by run.py). A case is VALID when none of its runs errored; only valid cases
enter the means. Reports, per arm and paired per case: mean score, turns, cost per run, and a cost-adjusted score
(mean score divided by mean cost per run in cents). With --compare, the `with` arm of DIR is set against the `with`
arm of OTHER_DIR on the cases valid in both (an A/B of two plugin versions).
"""
import json, glob, os, sys, statistics as st, csv


def load(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.json"))):
        try:
            doc = json.load(open(p))
        except ValueError:
            continue
        for c in doc.get("cases", []):
            out[c["name"]] = c
    return out


def arm(c, name):
    runs = c.get("arms", {}).get(name, [])
    return runs


def stats(runs):
    sc = [(r.get("score") or 0) for r in runs]
    return dict(score=st.mean(sc) if sc else None, turns=st.mean([r.get("turns") or 0 for r in runs]) if runs else None,
                cost=st.mean([r.get("costUsd") or 0 for r in runs]) if runs else None, n=len(runs),
                err=sum(1 for r in runs if r.get("error")))


def valid(c):
    return all(not r.get("error") for a in c.get("arms", {}).values() for r in a) and any(c.get("arms", {}).values())


def pct(a, b):
    return 100 * (a / b - 1) if b else float("nan")


def main(argv):
    if not argv:
        print(__doc__); return 1
    d = argv[0]
    csvp = argv[argv.index("--csv") + 1] if "--csv" in argv else None
    other = argv[argv.index("--compare") + 1] if "--compare" in argv else None
    cases = load(d)
    ok = {n: c for n, c in cases.items() if valid(c)}
    bad = sorted(n for n in cases if n not in ok)
    print(f"{len(cases)} cases, {len(ok)} valid, {len(bad)} with errored runs")
    rows = []
    for n, c in sorted(ok.items()):
        w, o = stats(arm(c, "with")), stats(arm(c, "without"))
        rows.append((n, w, o))
    paired = [(n, w, o) for n, w, o in rows if w["score"] is not None and o["score"] is not None]
    if paired:
        mw = st.mean(w["score"] for _, w, _ in paired); mo = st.mean(o["score"] for _, _, o in paired)
        imp = sum(1 for _, w, o in paired if w["score"] - o["score"] >= .10); wor = sum(1 for _, w, o in paired if o["score"] - w["score"] >= .10)
        tw = st.mean(w["turns"] for _, w, _ in paired); to = st.mean(o["turns"] for _, _, o in paired)
        cw = st.mean(w["cost"] for _, w, _ in paired); co = st.mean(o["cost"] for _, _, o in paired)
        print(f"paired over {len(paired)} valid cases: with {mw:.3f}, without {mo:.3f} (delta {mw-mo:+.3f}); "
              f"improve {imp}, worse {wor}, tie {len(paired)-imp-wor}; turns {pct(tw,to):+.0f}%, cost {pct(cw,co):+.0f}%")
        print(f"cost-adjusted (score per cent of cost per run): with {mw/(cw*100):.1f}, without {mo/(co*100):.1f}")
    if other:
        oc = {n: c for n, c in load(other).items() if valid(c)}
        both = [n for n in ok if n in oc]
        if both:
            a = [stats(arm(ok[n], "with")) for n in both]; b = [stats(arm(oc[n], "with")) for n in both]
            print(f"A/B on {len(both)} cases valid in both (A = {d}, B = {other}), arm 'with': "
                  f"score {st.mean(x['score'] for x in a):.3f} vs {st.mean(x['score'] for x in b):.3f}; "
                  f"turns {st.mean(x['turns'] for x in a):.1f} vs {st.mean(x['turns'] for x in b):.1f}; "
                  f"cost {st.mean(x['cost'] for x in a):.4f} vs {st.mean(x['cost'] for x in b):.4f}")
    if csvp:
        with open(csvp, "w", newline="") as f:
            w_ = csv.writer(f); w_.writerow(["case", "valid", "with", "without", "turns_with", "turns_without", "cost_with", "cost_without"])
            for n, c in sorted(cases.items()):
                ww, oo = stats(arm(c, "with")), stats(arm(c, "without"))
                w_.writerow([n, int(n in ok)] + [("%.3f" % x) if x is not None else "" for x in (ww["score"], oo["score"], ww["turns"], oo["turns"], ww["cost"], oo["cost"])])
    if bad:
        print("errored (re-run):", ", ".join(bad))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
