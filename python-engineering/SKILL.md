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

Read every file that matches the task before you write code. The files are in this skill's folder, not the project: open them with Read at the full path (this folder + the path); do not search for them. Paths start at `references/fields/software-engineering/`.

Every code change: `all/code/snags.md`, `all/workflow/shipping.md`. Then what the task touches:

- new function, class, option, constant, wrapper, naming: `all/code/minimalism.md`
- hand-rolling a utility, adding a package, an optional dependency (extra, lazy import): `all/code/stdlib-first.md`, `all/dependencies/dependencies.md`, `library/shared/api-design.md`
- raising, catching, batches that partly fail: `all/code/errors.md`; parsing input: `all/code/validation.md`
- annotations or checker errors: `all/code/typing.md`
- files, connections, locks, subprocesses, streams: `all/code/resources.md`
- a feature newer than the Python target: `all/code/python-versions.md`
- docstring or comment: `all/code/comments.md`
- logging, secrets, SQL, `eval`, `pickle`: `all/code/logging.md`, `all/code/security-basics.md`
- script or CLI: `all/code/scripts.md`
- tests: `all/testing/testing.md`
- slow or memory-heavy code, faster library: `all/performance/index.md`
- uv, locking, CI job, Dockerfile: `all/dependencies/uv.md`, `uv-ci.md`, `uv-docker.md`
- planning, scope, when to stop: `all/workflow/planning.md`; a bug: `all/workflow/debugging.md`
- a library others install: public name, signature, exception, extra: `library/shared/api-design.md`; new package, pyproject, layout, CI: `library/shared/package-setup.md`, `layout.md`; version, release: `library/shared/versioning.md`, `release.md`
- an HTTP service (endpoints, auth, database, deploy): `application/apis/http/services.md`; auth, tokens, CORS, uploads: `application/apis/shared/security.md`
- async code, request handlers, caches: `application/shared/async.md`, `application/shared/service-snags.md`
- background jobs, queues, schedulers: `application/workers/background-jobs.md`
- logs, metrics, traces, health checks: `application/shared/observability.md`
- settings, environment variables, secrets in config: `application/shared/configuration.md`
- timeouts, retries, circuit breakers: `application/shared/resilience.md`
- a pattern, new layers, an extension point, a settings object: `../software-architecture/design-patterns.md`

Other project kinds: `references/which-type.md`, then the `index.md` of each path in `kind`. A path with no folder: say no specialist guidance exists.
