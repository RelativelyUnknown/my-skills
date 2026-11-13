#!/usr/bin/env python3
"""smellcheck.py: AST checks for the smells ruff does not catch, and a self-test over before/after example pairs.

    python3 tools/eval/smellcheck.py FILE.py [FILE.py ...]     print `file:line rule` for each hit
    python3 tools/eval/smellcheck.py --selftest                 every smell_pairs/<rule>.bad.py must hit <rule>, every .good.py nothing

Rules (each matches a row in tabby/development/code/smells.md): deep-nesting (control flow more than three levels inside a
function), unbounded-cache (functools.cache, or lru_cache with maxsize=None), validated-mutable-dataclass (a non-frozen
dataclass with __post_init__ validation, so callers can later set a field past the rule), match-on-bool (match with True or
False patterns), stub-override (a method that only raises NotImplementedError or passes, in a class that has a base and is
not abstract), sentinel-return (`return -1`). Heuristics, stdlib only: a hit is a lead, not a verdict.
"""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEST = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.With, ast.AsyncWith, ast.Match)


def _name(node):
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Call):
        return _name(node.func)
    return ""


def _kw(call, key):
    return next((k.value for k in getattr(call, "keywords", []) if k.arg == key), None)


def check(tree):
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                n = _name(dec)
                if n == "cache" or (n == "lru_cache" and isinstance(dec, ast.Call)
                                    and isinstance(_kw(dec, "maxsize"), ast.Constant) and _kw(dec, "maxsize").value is None):
                    hits.append((dec.lineno, "unbounded-cache"))
            deepest = [0, 0]

            def walk(n, depth):
                for ch in ast.iter_child_nodes(n):
                    d = depth + 1 if isinstance(ch, NEST) else depth
                    if d > deepest[0]:
                        deepest[:] = [d, getattr(ch, "lineno", node.lineno)]
                    walk(ch, d)
            walk(node, 0)
            if deepest[0] > 3:
                hits.append((deepest[1], "deep-nesting"))
            for r in ast.walk(node):
                if isinstance(r, ast.Return) and isinstance(r.value, ast.UnaryOp) and isinstance(r.value.op, ast.USub) \
                        and isinstance(r.value.operand, ast.Constant) and r.value.operand.value == 1:
                    hits.append((r.lineno, "sentinel-return"))
        if isinstance(node, ast.ClassDef):
            for dec in node.decorator_list:
                if _name(dec) == "dataclass":
                    frozen = _kw(dec, "frozen") if isinstance(dec, ast.Call) else None
                    is_frozen = isinstance(frozen, ast.Constant) and frozen.value is True
                    has_post = any(isinstance(b, ast.FunctionDef) and b.name == "__post_init__" for b in node.body)
                    if has_post and not is_frozen:
                        hits.append((node.lineno, "validated-mutable-dataclass"))
            real_bases = [b for b in node.bases if _name(b) not in ("ABC", "Protocol", "object", "Exception")]
            abstract = any(_name(b) in ("ABC", "Protocol") for b in node.bases)
            if real_bases and not abstract:
                for f in node.body:
                    if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) and not f.name.startswith("__"):
                        body = [s for s in f.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
                        if len(body) == 1 and (isinstance(body[0], ast.Pass) or (
                                isinstance(body[0], ast.Raise) and "NotImplementedError" in ast.dump(body[0]))):
                            hits.append((f.lineno, "stub-override"))
        if isinstance(node, ast.Match):
            for case in node.cases:
                p = case.pattern
                if isinstance(p, ast.MatchSingleton) and isinstance(p.value, bool):
                    hits.append((node.lineno, "match-on-bool"))
                    break
    return sorted(set(hits))


def check_file(path):
    try:
        return check(ast.parse(open(path, errors="ignore").read()))
    except (SyntaxError, ValueError):
        return []


def selftest():
    d = os.path.join(HERE, "smell_pairs")
    bad = good = 0
    problems = []
    for f in sorted(os.listdir(d)):
        rule, kind = f.rsplit(".", 2)[0], f.rsplit(".", 2)[1]
        rules = {r for _, r in check_file(os.path.join(d, f))}
        if kind == "bad":
            if rule not in rules:
                problems.append(f"{f}: expected {rule}, got {sorted(rules)}")
            bad += 1
        elif kind == "good":
            if rules:
                problems.append(f"{f}: expected nothing, got {sorted(rules)}")
            good += 1
    print(f"{bad} bad and {good} good examples; {len(problems)} problems")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    for p in sys.argv[1:]:
        for line, rule in check_file(p):
            print(f"{p}:{line} {rule}")
