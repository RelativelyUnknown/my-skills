# Development

Defaults: the `## Python defaults` section of AGENTS.md: `kind`, `python`, `runner`, `types`, `layout`, `rigor` (lite, full, ultra), `report` (terse, normal, audit), `docstrings`. Infer gaps from the repo (grep `pyproject.toml`, lockfiles, CI). Ask only what is still unknown, once, with your question tool if you have one, and save the answers there. Cannot ask: use defaults, mark them `(assumed)`, say so in your report.

## Never miss

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green. A test that contradicts the spec: leave it, finish the rest, report it.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- Do not silence tools (`# type: ignore`, `# noqa`, `cast`, `Any`, looser config); fix the cause.
- Smallest diff that solves it properly. No new dependency, public API change, commit or push unasked.
- Use the project's own tools and Python target; never install silently.
- Replies, comments and docs are short: what is not obvious, no filler or praise. Never drop "not", "never", "only", "except".

## Read before you write

Read every file matching the task before writing code. The paths below start at `development/` inside the tabby skill folder: `code/smells.md` is `development/code/smells.md`. Open each with Read; do not search. Always: `code/smells.md`, `workflow/shipping.md`. Then:

- new function, class, option, constant, wrapper, name: `code/minimalism.md`
- hand-rolled utility, new package, optional dependency (extra, lazy import): `code/stdlib-first.md`, `dependencies/dependencies.md`, `library/shared/api-design.md`
- raising, catching, partial failure: `code/errors.md`; parsing input: `code/validation.md`
- annotations, checker errors: `code/typing.md`
- files, connections, locks, subprocesses, streams: `code/resources.md`
- feature newer than the Python target: `code/python-versions.md`
- docstring, comment: `code/comments.md`
- logging, secrets, SQL, `eval`, `pickle`: `code/logging.md`, `code/security-basics.md`
- script or CLI: `code/scripts.md`
- tests: `testing/testing.md`, `testing/smells.md`
- slow code: `performance/index.md`
- uv, locking, CI job, Dockerfile: `dependencies/uv.md`, `uv-ci.md`, `uv-docker.md`
- scope, when to stop: `workflow/planning.md`; a bug: `workflow/debugging.md`; restructuring code: `workflow/refactoring.md`; an API you are unsure of: `workflow/checking-apis.md`
- a library others install: `library/smells.md`, `library/shared/package-setup.md`, `layout.md`, `versioning.md`, `release.md`; with Rust, C or Cython behind a Python API: `library/native/index.md`, `library/native/smells.md`
- retries, timeouts, backoff, circuit breakers: `application/shared/resilience.md`
- a service: `application/smells.md`, `application/apis/http/services.md`, `application/apis/shared/security.md`, `application/shared/async.md`, `observability.md`, `configuration.md`; workers: `application/workers/background-jobs.md`
- pattern, layers, extension point, settings object: `architecture/design-patterns.md`
- choosing a data structure, representation or algorithm (Rust, C, C++ or Python): `architecture/fit.md`, `architecture/fit-examples.md`, `architecture/senior-engineering.md`

Other project kinds: `development/which-type.md`, then each `kind` path's `index.md` (kind paths start at `development/`).
