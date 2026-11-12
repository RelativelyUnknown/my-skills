#!/usr/bin/env python3
"""selftest.py: prove check.py can fail. Python standard library only.

    python3 selftest.py

Gate 1: every file in examples/ passes (exit 0).
Gate 2 (negative controls): each seeded defect below makes check.py report the rule it targets.
A checker that cannot fail would pass everything, so the second gate is the one that matters.
Exit 0 if all hold, 1 otherwise.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check.py")
BASE = open(os.path.join(HERE, "examples", "service-request.svg"), encoding="utf-8").read()


def sub1(text, pattern, repl):
    out, n = re.subn(pattern, repl, text, count=1)
    assert n == 1, f"mutation did not apply: {pattern}"
    return out


MUTATIONS = {
    "a11y-title": lambda s: sub1(s, r"<title[^>]*>.*?</title>\n", ""),
    "diagonal": lambda s: sub1(s, r'(data-edge="client&gt;api"[^>]*? d=")[^"]*"', r'\1M180,272 L284,300"'),
    "node-overlap": lambda s: s.replace("</svg>", '<g data-node="extra"><rect data-box="1" x="900" y="428" width="80" height="40"/></g>\n</svg>'),
    "edge-through-node": lambda s: s.replace("</svg>", '<g data-node="extra"><rect data-box="1" x="684" y="340" width="32" height="32"/></g>\n</svg>'),
    "pill-clearance": lambda s: sub1(s, r'(data-pill="api&gt;queue"><rect x=")\d+(" y="\d+" width=")\d+"', r'\g<1>436\g<2>112"'),
    "tiny-text": lambda s: sub1(s, r'font-size="15">Work', 'font-size="8">Work'),
    "budget": lambda s: s.replace('<g data-node="api">', '<g data-node="api" data-focal="1">').replace('<g data-node="worker">', '<g data-node="worker" data-focal="1">'),
    "contrast": lambda s: sub1(s, r"--label:#5B6270", "--label:#B0B6C3"),
    "viewbox": lambda s: s.replace("</svg>", '<g data-node="extra"><rect data-box="1" x="1000" y="40" width="100" height="40"/></g>\n</svg>'),
}


def run(path):
    p = subprocess.run([sys.executable, CHECK, path], capture_output=True, text=True)
    return p.returncode, p.stdout


def main():
    ok = True
    ex = os.path.join(HERE, "examples")
    for name in sorted(f for f in os.listdir(ex) if f.endswith(".svg")):
        code, out = run(os.path.join(ex, name))
        print(("PASS" if code == 0 else "FAIL"), "example clean:", name)
        if code != 0:
            ok = False
            print(out)
    with tempfile.TemporaryDirectory() as tmp:
        for rule, mutate in MUTATIONS.items():
            path = os.path.join(tmp, f"{rule}.svg")
            try:
                open(path, "w", encoding="utf-8").write(mutate(BASE))
            except AssertionError as err:
                print("FAIL control", rule, "->", err)
                ok = False
                continue
            code, out = run(path)
            hit = f"FAIL {rule} " in out
            others = sorted({m for m in re.findall(r"^FAIL (\S+) ", out, re.M) if m != rule})
            print(("PASS" if hit and code == 2 else "FAIL"), "control trips", rule, ("(also: " + ", ".join(others) + ")") if others else "")
            if not (hit and code == 2):
                ok = False
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
