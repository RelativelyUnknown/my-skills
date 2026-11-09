---
name: python-engineering
description: "Rules for every Python code change: errors, minimalism, stdlib first, typing, tests, dependencies, uv, CI, packaging, performance, docs, Rust and C extensions. Use whenever you write, change, debug, test, speed up, package or release Python; load before editing any .py or pyproject.toml file."
license: MIT
---

# Python engineering

Defaults live in the `## Python defaults` section of AGENTS.md: `kind`, `python`, `runner`, `types`, `layout`, `rigor` (lite, full, ultra), `report` (terse, normal, audit), `docstrings`. Infer gaps from the repo (grep `pyproject.toml`, lockfiles, CI). Ask only what is still unknown, once, with your question tool if you have one, and save the answers there. Cannot ask: use sensible defaults, mark them `(assumed)`, say so in your report.

## Never miss

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green. A test that contradicts the spec: leave it, finish the rest, report it.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- Do not silence tools (`# type: ignore`, `# noqa`, `cast`, `Any`, looser config); fix the cause.
- Smallest diff that solves it properly. No new dependency, public API change, commit or push unasked.
- Use the project's own tools and Python target; never install silently.
- Replies, comments and docs are short: what is not obvious, no filler or praise. Never drop "not", "never", "only", "except".

## Read before you write

Read every file matching the task before writing code. Open them with Read at this folder plus the path; do not search. Paths start at `references/fields/software-engineering/`. Always: `all/code/snags.md`, `all/workflow/shipping.md`. Then:

- new function, class, option, constant, wrapper, name: `all/code/minimalism.md`
- hand-rolled utility, new package, optional dependency (extra, lazy import): `all/code/stdlib-first.md`, `all/dependencies/dependencies.md`, `library/shared/api-design.md`
- raising, catching, partial failure: `all/code/errors.md`; parsing input: `all/code/validation.md`
- annotations, checker errors: `all/code/typing.md`
- files, connections, locks, subprocesses, streams: `all/code/resources.md`
- feature newer than the Python target: `all/code/python-versions.md`
- docstring, comment: `all/code/comments.md`
- logging, secrets, SQL, `eval`, `pickle`: `all/code/logging.md`, `all/code/security-basics.md`
- script or CLI: `all/code/scripts.md`; tests: `all/testing/testing.md`
- slow code, faster library: `all/performance/index.md`
- uv, locking, CI job, Dockerfile: `all/dependencies/uv.md`, `uv-ci.md`, `uv-docker.md`
- scope, when to stop: `all/workflow/planning.md`; a bug: `all/workflow/debugging.md`
- library others install: public name, signature, exception, extra: `library/shared/api-design.md`; new package, pyproject, layout, CI: `library/shared/package-setup.md`, `layout.md`; version, release: `versioning.md`, `release.md`
- HTTP service: `application/apis/http/services.md`; auth, tokens, CORS, uploads: `application/apis/shared/security.md`
- async, request handlers, caches: `application/shared/async.md`, `service-snags.md`
- queues, schedulers: `application/workers/background-jobs.md`
- logs, metrics, traces, health: `application/shared/observability.md`; settings, env, secrets: `configuration.md`; timeouts, retries: `resilience.md`
- pattern, layers, extension point, settings object: `../software-architecture/design-patterns.md`
- Rust, C or C++ behind a Python API, PyO3, maturin, cibuildwheel: `library/native/index.md`, then `architecture.md` and the leaf for the language
- README, docstring, API reference, tutorial, how-to, changelog, ADR, runbook, troubleshooting, CONTRIBUTING: `../documentation/workflow.md`, then `../documentation/index.md`
- diagram or explainer animation: the `python-design` skill; a review or audit: the `python-review` skill
- starting a project or no `## Tabby` section in AGENTS.md: the `tabby` skill

Other project kinds: `references/which-type.md`, then each `kind` path's `index.md`. A path with no folder: say no specialist guidance exists.
