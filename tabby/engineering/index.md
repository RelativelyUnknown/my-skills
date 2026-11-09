# Engineering

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

Read every file matching the task before writing code. The paths below start at `engineering/references/fields/software-engineering/` inside the tabby skill folder: `all/code/snags.md` is `engineering/references/fields/software-engineering/all/code/snags.md`. Open each with Read; do not search. Always: `all/code/snags.md`, `all/workflow/shipping.md`. Then:

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
- a library others install: `library/shared/package-setup.md`, `layout.md`, `versioning.md`, `release.md`; with Rust, C or Cython behind a Python API: `library/native/index.md`
- a service: `application/apis/http/services.md`, `application/apis/shared/security.md`, `application/shared/async.md`, `service-snags.md`, `observability.md`, `configuration.md`, `resilience.md`; workers: `application/workers/background-jobs.md`
- pattern, layers, extension point, settings object: `engineering/references/fields/software-architecture/design-patterns.md`

Other project kinds: `engineering/references/which-type.md`, then each `kind` path's `index.md` (kind paths start at `engineering/references/fields/`).
