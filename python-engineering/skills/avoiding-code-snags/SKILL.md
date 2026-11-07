---
name: avoiding-code-snags
description: "Catalogue of Python code snags, ranked blocker, wince or nit, each with its fix and the lint rule that catches it, including what a caller sees in a hover tooltip. Use when asked to review a Python file or module for problems, list what is wrong worst first, clean up a file, or check your own diff before saying done."
argument-hint: "[python=3.12 report=normal]"
---

# Avoiding code snags

A snag is a small thing that catches the reader's eye and makes them stop: the code runs, but it is wrong, noisy or misleading. This is a recognition aid for review and cleanup, not a second rulebook. The rules and their reasons are in `writing-python-code` (Errors, Minimalism, Types, names, structure); each snag below gives the fix in one line. Use it when asked to review or clean up, or before reporting done. Do not apply it to ordinary feature work.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`python.target`, `types`, `lint`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Use fixes available at `python.target`.

## Severity

- **Blocker:** wrong or hidden behavior. Swallowed errors, mutable defaults, naive time, `assert` as validation, secrets in code, injection, a network call with no timeout, a call in a default argument.
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
- A literal default in the signature, a `Literal[...]` option, and a constant that the body uses (`MAX_BODY_BYTES`).
- `print` in a command-line entry point whose job is to print.
- `Any` or `object` at a true boundary (network JSON) that is narrowed at once.

## Snags

Format: snag (severity): what it looks like → fix (lint rule, when one exists).

- Swallowed error (blocker): `except Exception: pass`, or a default returned from `except` → catch the named error, or let it propagate (S110, BLE001)
- Assert as validation (blocker): `assert isinstance(d, dict)` → `if not ...: raise ValueError(...)`; asserts vanish under `python -O` (S101)
- Mutable default (blocker): `def f(rows=[])` → `None`, build in the body (B006)
- Naive time (blocker): `datetime.utcnow()`, `datetime.now()` → `datetime.now(UTC)` (DTZ003, DTZ005)
- Log and re-raise (wince): `logger.error(e)` then `raise` → log once at the boundary, or raise
- Clobbering default (wince): `timeout = timeout or 30` replaces `0` → `if timeout is None`
- Masked missing data (wince): `payload.get("name", "")` or `getattr(obj, "x", None)` for a field that must exist → `payload["name"]`, so a missing field fails where it happens
- Module-level mutable state (wince): `_CACHE = {}` → pass it in, or `functools.cache`
- Untyped bag (wince): `dict[str, Any]` passed around, a bare `-> dict` → dataclass or `TypedDict` (ANN401)
- Positional boolean (wince): `run(path, True, False)` → keyword-only (FBT001, FBT002)
- Tuple of 3+ returned (wince): `return a, b, c` → a named structure
- Stateless class (wince): `class FooManager` with an empty `__init__` and one method → a function
- One-line wrapper (wince): `def quote(s): return f'"{s}"'` → inline it
- One-implementation ABC, factory or registry (wince):  → the function or class itself
- `utils.py`, `helpers.py`, `common.py` (wince):  → put the code where it is used
- Vague or versioned name (wince): `data`, `result`, `new_`, `v2`, `final`, `Handler` → name what it is
- Narrating docstring or comment (wince): "This module ingests reports", `# Step 1: open the file` → say what is not obvious, or delete
- Restated signature (wince): `:param x: the x (int)` → omit
- Conversation residue (wince): "as discussed", "now uses", "previously" → move to the commit message
- Inflated claim (wince): "robust", "comprehensive", "production-ready" → state the fact
- Leftover debugging (wince): `print(...)` in library code, `TODO` litter → delete, or use `logging` (T201, FIX)
- Defensive code for the impossible (wince): a guard no caller can trigger → delete
- Duplicate of an existing helper (wince): wrote a new one without searching → use the existing one (`rg`)
- No timeout (blocker): `urlopen(url)`, `requests.get(url)`; a `timeout` parameter that is never passed on → pass an explicit timeout (S113)
- `open()` without encoding (wince): `open(path)` reads in the machine's locale → `open(path, encoding="utf-8")` (PLW1514)
- Import-time side effects (wince): `os.environ[...]`, `logging.basicConfig()`, a connection or background work at module level → do it in a function at the program edge
- Generic exception (wince): `raise Exception("bad status")`, or re-raising a new error without `from e` → a specific built-in or `PkgError`; `raise ... from e` (TRY002, B904)
- Unexplained number (nit): `items[:37]` with no name or reason → name it if it carries meaning, or comment why; never to hide a signature default
- Test that cannot fail (wince): `assert result is not None`, only the mock was called → see `testing-python-packages` (PT)
- Resource not reliably closed (wince): `f.close()` that an early `return` skips; a reader returned from inside its `with` → `with`, and consume iterators while it is open (sqlite3's `with` does not close) (SIM115)
- `try` block too broad (wince): one `try` around many steps, catching `KeyError` → wrap only the line expected to raise; use `else`
- Detached task (blocker when work or errors are lost): `asyncio.create_task(job())`, result dropped → `TaskGroup`, or keep the task and collect its exception (RUF006)
- New client per call (wince): `httpx.AsyncClient()` created per request → one per application lifespan
- Session shared by concurrent tasks (blocker): one `AsyncSession` passed to `gather()` tasks → one session per task

## What the caller sees

Hover tooltips and signature help show the signature, not the body, so these snags cost every caller, not only the maintainer.

- Constant as default (wince): `def f(timeout=DEFAULT_TIMEOUT)`: hover shows a name, not the value → `timeout: float = 30`
- `None` hiding the real default (wince): `retries=None`, then `retries = retries or 3` → the real default in the signature
- Call in a default (blocker): `def stamp(now=datetime.now())` runs once, at import → `None` and build it in the body, or a required argument (B008)
- Hidden parameters (wince): `def request(url, **kwargs)` → name them; `Unpack[TypedDict]` for many options
- Wrapper without `functools.wraps` (wince): hover shows `(*args, **kwargs)` and the docstring is lost → `@functools.wraps(func)`, or `ParamSpec`
- Option as a free string (wince): `mode="strict"` → `Literal["strict", "lenient"]`, so hover lists the choices
- Builtin as a parameter name (wince): `def get(id, type)` → `item_id`, `kind` (A002)
- Wide positional signature (wince): six or more positional parameters → keyword-only after `*`, or a dataclass (PLR0913)

## Read when relevant

- Untrusted input, files or connections, subprocesses, retries, tests, package structure: [snags-reliability.md](references/snags-reliability.md)
- Async code, caches, request handlers, background work, API documentation: [snags-services.md](references/snags-services.md)
