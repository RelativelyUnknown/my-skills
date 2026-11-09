---
name: python-engineering
description: "Rules for every Python code change: errors, minimalism, standard library first, typing, tests, dependencies and uv, CI, packaging, performance, reporting. Use whenever you write, modify, debug, test, speed up, package or release Python; load before editing any .py or pyproject.toml file."
license: MIT
---

# Python engineering

Defaults: read the `## Python defaults` section of AGENTS.md. Infer what is missing from the repo with grep (`pyproject.toml`, lockfiles, CI). Ask only what is still unknown, once, with your interactive question tool if you have one (otherwise one short message listing the options), then add the answers to that section (create it if absent). If you cannot ask, use sensible defaults, mark them `(assumed)` and say so in your report.

Keys: `kind`, `python`, `runner`, `types`, `layout`, `rigor` (lite, full, ultra), `report` (terse, normal, audit), `docstrings`.

## Never miss

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green. A test that contradicts the spec: leave it, finish the rest, report it.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- Do not silence tools to pass (`# type: ignore`, `# noqa`, `cast`, `Any`, looser config); fix the cause.
- Smallest diff that solves it properly. No new dependency, public API change, commit or push unasked.
- Use the project's own tools and the Python target; never install silently.
- Replies, comments and docs are short: say what is not obvious, no filler or praise words. Never drop "not", "never", "only", "except".

## Read before you write

The files below are in this skill's folder, not the project. Open them with Read at the full path (this folder + the path); do not search for them. Paths start at `references/fields/software-engineering/all/`.

Every code change: `code/snags.md`, `workflow/shipping.md`. Then what the task touches:

- new function, class, option, constant, wrapper, naming: `code/minimalism.md`
- hand-rolling a utility, adding a package: `code/stdlib-first.md`, `dependencies/dependencies.md`
- raising, catching, batches that partly fail: `code/errors.md`; parsing input: `code/validation.md`
- annotations or checker errors: `code/typing.md`
- files, connections, locks, subprocesses, streams: `code/resources.md`
- a feature newer than the Python target: `code/python-versions.md`
- docstring or comment: `code/comments.md`
- logging, secrets, SQL, `eval`, `pickle`: `code/logging.md`, `code/security-basics.md`
- script or CLI: `code/scripts.md`
- tests: `testing/testing.md`
- slow or memory-heavy code, faster library: `performance/index.md`
- uv, locking, CI job, Dockerfile: `dependencies/uv.md`, `uv-ci.md`, `uv-docker.md`
- planning, scope, when to stop: `workflow/planning.md`; a bug: `workflow/debugging.md`

## Project kind

For a library others install, read `references/fields/software-engineering/library/shared/index.md`; for async, request handlers or caches, `.../application/shared/index.md`; for patterns, layers or extension points, `references/fields/software-architecture/index.md`. Other kinds: `references/which-type.md`, then the `index.md` of each path in `kind`. A path with no folder: say no specialist guidance exists.
