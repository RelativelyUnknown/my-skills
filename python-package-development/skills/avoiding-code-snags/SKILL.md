---
name: avoiding-code-snags
description: "Catalogue of Python code snags, the small things that make a reviewer wince, ranked blocker, wince or nit, each with its fix and the lint rule that catches it. Use when cleaning up a file, reviewing code for smells or AI slop, or checking your own diff before saying done."
argument-hint: "[python=3.12 report=normal]"
---

# Avoiding code snags

A snag is a small thing that catches the reader's eye and makes them stop: the code runs, but it is wrong, noisy or misleading. This is a recognition aid for review and cleanup, not a second rulebook. The rules and their reasons are in `writing-python-code` (Errors, Minimalism, Types, names, structure); each snag below gives the fix in one line. Use it when asked to review or clean up, or before reporting done. Do not apply it to ordinary feature work.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`python.target`, `types`, `lint`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Use fixes available at `python.target`.

## Severity

- **Blocker:** wrong or hidden behavior. Swallowed errors, mutable defaults, naive time, `assert` as validation, secrets in code, injection, a load that duplicates rows when re-run.
- **Wince:** misleads or burdens the reader. Everything marked wince below.
- **Nit:** tidy-up the linter already knows (unused imports, `== None`, `== True`, `len(x) == 0`, commented-out code, wildcard imports). Fix them in a cleanup; never list them in a review.

## Modes

- **Review:** change nothing. One line per snag, worst first: `file:line  severity  snag: fix`. Merge repeats ("`print` on lines 12, 30, 41"). At most 30 lines, 10 for `report=terse`. End with `Fine as written:` and what you checked and deliberately left.
- **Cleanup:** fix every blocker and wince in the named file, nits too, with the smallest diff. No unrelated changes, no new files, keep the tests passing, and report what you left alone and why.

## Fine as written, do not flag

- `except FileNotFoundError: return None` when the docstring says absence is a normal answer.
- `# type: ignore[code]` or `# noqa: CODE` with a reason in the comment.
- A helper that hides real logic (parsing, validation, a rule that must stay consistent).
- A class with state that persists across calls or an invariant its methods protect.
- `print` in a command-line entry point whose job is to print.
- `Any` or `object` at a true boundary (network JSON) that is narrowed at once.

## Snags

| Snag | Looks like | Fix | Catch |
| --- | --- | --- | --- |
| Swallowed error (blocker) | `except Exception: pass`, or a default returned from `except` | catch the named error, or let it propagate | S110, BLE001 |
| Assert as validation (blocker) | `assert isinstance(d, dict)` | `if not ...: raise ValueError(...)`; asserts vanish under `python -O` | S101 |
| Mutable default (blocker) | `def f(rows=[])` | `None`, build in the body | B006 |
| Naive time (blocker) | `datetime.utcnow()`, `datetime.now()` | `datetime.now(UTC)` | DTZ003, DTZ005 |
| Log and re-raise (wince) | `logger.error(e)` then `raise` | log once at the boundary, or raise | grep |
| Clobbering default (wince) | `timeout = timeout or 30` replaces `0` | `if timeout is None` | grep |
| Module-level mutable state (wince) | `_CACHE = {}` | pass it in, or `functools.cache` | grep |
| Untyped bag (wince) | `dict[str, Any]` passed around | dataclass or `TypedDict` | ANN401 |
| Positional boolean (wince) | `run(path, True, False)` | keyword-only | FBT001, FBT002 |
| Tuple of 3+ returned (wince) | `return a, b, c` | a named structure | grep |
| Stateless class (wince) | `class FooManager` with an empty `__init__` and one method | a function | grep |
| One-line wrapper (wince) | `def quote(s): return f'"{s}"'` | inline it | grep |
| One-implementation ABC, factory or registry (wince) | | the function or class itself | grep |
| `utils.py`, `helpers.py`, `common.py` (wince) | | put the code where it is used | name |
| Vague or versioned name (wince) | `data`, `result`, `new_`, `v2`, `final`, `Handler` | name what it is | name |
| Narrating docstring or comment (wince) | "This module ingests reports", `# Step 1: open the file` | say what is not obvious, or delete | grep |
| Restated signature (wince) | `:param x: the x (int)` | omit | review |
| Conversation residue (wince) | "as discussed", "now uses", "previously" | move to the commit message | grep |
| Inflated claim (wince) | "robust", "comprehensive", "production-ready" | state the fact | grep |
| Leftover debugging (wince) | `print(...)` in library code, `TODO` litter | delete, or use `logging` | T201, FIX |
| Defensive code for the impossible (wince) | a guard no caller can trigger | delete | review |
| Duplicate of an existing helper (wince) | wrote a new one without searching | use the existing one | `rg` |
| Test that cannot fail (wince) | `assert result is not None`, only the mock was called | see `testing-python-packages` | PT |
