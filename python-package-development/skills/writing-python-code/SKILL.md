---
name: writing-python-code
description: "Rules for writing and changing Python source: error handling, minimalism, standard library first, typing, naming, docstrings, logging, security, complexity advice, and the end-of-task report. Use when writing, modifying, refactoring or debugging Python code."
argument-hint: "[python=3.12 runner=uv types=mypy report=normal]"
---

# Writing Python code

Aim for the fewest concepts a reader must learn, not the fewest characters. Write like a senior engineer who golfs, never at the cost of clarity. If a rule conflicts with the request, say so and ask.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root. It prints the project's facts (`python.target`, `runner`, `types`, `lint`, `tools.missing`, ...); `# default` means nothing was found.

- Arguments (`key=value` after the skill name) override detected facts: argument, then detected, then default.
- Prefix commands with the detected `runner`. Keep the project's existing tools (poetry, black, pyright, ...); never add a second tool for the same job.
- Report `tools.missing`; never install a tool or dependency silently.

## Done and stopping

- Done means the real problem is solved, verified by running the code, and explainable. Passing tests are evidence, not the goal.
- Before a non-trivial change, state the approach in a few lines. Read the code and its callers before changing it; find every caller (code, tests, scripts, config, docs) before renaming or changing a signature.
- State the cause of a bug in one sentence before fixing it; if you cannot, investigate. Never special-case inputs or hardcode expected outputs. No sleeps, retries or longer timeouts until the cause of a race is known. Do not pin, downgrade or swap a dependency, or edit `sys.path`, to get past an error without explaining why.
- After two or three failed attempts at the same fix, stop guessing: re-read the code, state a hypothesis, then act.
- **Stop and report** instead of working around a problem when a test contradicts the spec or task; the task cannot be done properly with the code and dependencies available; the fix needs a new dependency, a public API change or a deleted file; or you catch yourself justifying test-specific behavior with a reason like "backward compatibility". Ask first when requirements are ambiguous and a wrong guess is expensive.
- Smallest diff that solves the problem properly. No unrelated refactors, renames or reformatting; mention what you noticed. No summary, changelog or demo files nobody asked for; delete scratch files. Do not edit CI, lint or pytest config unless that is the task.
- Do not commit, push or run destructive commands (`git reset --hard`, `rm -rf`, force-push, dropping tables) unless asked. Never skip hooks with `--no-verify`. Deleting data or files, dropping columns, changing a public API or irreversible migrations need approval first.
- Tests: see the `testing-python-packages` skill. Never edit an existing test to get green.

## Do not silence the tools

No `# type: ignore`, `# noqa`, `cast()` or `Any` to quiet a checker; fix the cause. If an ignore is truly needed, name the code (`# type: ignore[arg-type]`) and say why in a comment. Never disable a lint rule or loosen linter, type-checker or pytest config to make an error go away.

## Read when relevant

| Doing | Read |
| --- | --- |
| Using a feature that might be newer than `python.target` | [references/python-versions.md](references/python-versions.md) |
| Writing or changing a docstring or comment | [references/docs-and-comments.md](references/docs-and-comments.md) |
| Adding logging, reading secrets, touching SQL, subprocesses, `eval` or `pickle` | [references/logging-and-security.md](references/logging-and-security.md) |
| `xenon`, `radon` or a complexity lint rule reports a rank | [references/complexity-tools.md](references/complexity-tools.md) |
| Hand-rolling a utility | [references/stdlib-first.md](references/stdlib-first.md) |

Use features available at `python.target` and nothing newer; no `sys.version_info` branches or backports unless a dependency requires them. A target below 3.10 is end of life: ask first.

## Errors

- No bare `except:`. No `except Exception:` except at a top-level boundary that logs or reports and then re-raises or exits. Never `except: pass`.
- Catch narrowly, close to the source. Keep `try` blocks short; the success path goes in `else`.
- Never return `None`, `[]`, `{}` or `""` from an except block so the caller appears to work. Absence that is a normal answer is handled by name (`except FileNotFoundError`) and documented.
- Required data crashes when missing: `d["key"]`, not `d.get("key", "")`. No silent fallbacks: no stub imports, no defaults that mask missing config, no mock data in production code.
- No `hasattr`, `getattr` or `isinstance` to paper over an unknown type; find out what the type is.
- Let library exceptions propagate. Add a custom exception only when callers must handle a condition no existing exception expresses; wrap with `raise ... from e`, or attach context with `e.add_note(...)`.
- Error messages name the bad value, the valid choices and the fix: `f"unknown region {region!r}; expected one of {sorted(REGIONS)}"`.

## Minimalism

Every function, class, constant and exception is something a reader must look up. Each must earn its place.

- A function must hide real logic or enforce a rule that has to stay consistent. Deletion test: if inlining it leaves every call site as short and clear, delete it. No one-line wrappers around expressions, stdlib calls or library methods (`def quote(s): return f'"{s}"'`).
- A method that never reads `self` is a function; a class with `__init__` and one method is a function. No wrapper classes that only forward; no ABCs, Protocols, factories or registries with one implementation; no parameters, options or hooks "for flexibility"; no `**kwargs` unless forwarding.
- Defaults go in the signature or the dataclass field, never in a `DEFAULTS` dict. A shared immutable value may be a module constant (`DEFAULT_TIMEOUT = 30`); a value used once stays inline. Mutable defaults are never allowed: use `None` and build the object in the body.
- No `utils.py` or `helpers.py`; put code where it is used. No variable assigned only to be returned on the next line. No single-use type alias, base class or Enum "for consistency".
- Shorter only when also clearer: no nested comprehensions beyond one level, no walrus chains, no single-letter names outside tight loops.

## Use what exists

Order: the standard library, a dependency the project already has, a widely used community library, then your own code.

- Read `pyproject.toml` first. Before hand-rolling a utility, name the stdlib or library function you considered and why it does not fit.
- Use a library's features fully (`raise_for_status()`, pydantic validation). Never regex-parse structured formats: dates, URLs, HTML, JSON, CSV, versions.
- Add a dependency only if it is widely used and maintained and the stdlib or a few lines cannot do the job. Flag every new dependency in the report.
- Common jobs and what not to hand-roll: see the table above.

## Types, names, structure

- Structured data is a dataclass, `TypedDict` or the model class the project already uses, not a `dict[str, Any]` passed around. No `Any`: write the precise type, or `object` for a truly opaque value. `Optional` return only if the function can return `None`. No tuples of three or more values as a return type. No `x = x or 30` (`or` also replaces `0` and `""`).
- Names say what a thing is, in the codebase's vocabulary: `users`, not `user_list`. No vague names (`data`, `result`, `info`, `temp`, `obj`, `helper`, `manager`, `handler`), no `new_`/`old_`/`v2`/`final`/`fixed`/`robust`. Booleans read as predicates (`is_expired`). One word per concept: not `fetch`, `get` and `load` for the same thing.
- Core logic takes values and returns values; I/O and state stay at the edges. No module-level mutable state, singletons or global clients; pass dependencies in. Early returns over nesting. `with` for resources. Sets for membership checks in loops; batch queries and HTTP calls. Async code never calls blocking I/O, and a function that never awaits is not `async`.

## Report (`report=`, default `normal`)

Plain and factual. No "production-ready", "robust" or "comprehensive", no celebration, no emojis. Show the exact command and its real output; separate what you verified from what should work.

| Value | Contents |
| --- | --- |
| `terse` | Verdict, commands run with pass/fail counts, deviations. At most 10 lines. A new dependency, a changed or removed test, or a stopped task always counts as a deviation. |
| `normal` | What changed and why, commands with real output, verified vs unverified, every new dependency, every test changed or removed with the reason. |
| `audit` | `normal`, plus every shortcut, assumption, skipped check and known limitation (or "none"), everything noticed and left alone, and any rule conflict and which rule won. |
