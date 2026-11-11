# Development

Tool and style defaults are the `## Python defaults` section of AGENTS.md (`python`, `runner`, `build`, `test`, `lint`, `ci`, `types`, `rigor`, `report`, `docstrings`); the kind is `kind:` in `## Tabby`. Infer gaps from the repo; ask only what is still unknown; if you cannot ask, use defaults marked `(assumed)`.

## Work like a senior engineer

1. **Know the platform.** For each job, name what the language and ecosystem already give, in the order of `code/reuse.md` (the project's own tool, the standard library, the community's standard library, then niche or your own); `ecosystem.md` lists them by job. Check installed versions and the Python target (`workflow/checking-apis.md`); do not recall.
2. **Know the project.** Before the first edit, map it in about five commands: entry points, layers, how data is reached, the closest existing code to the ask, the most-changed files (`git log --name-only`), decisions (ADRs, `git log -S<name>`). With a `## Tabby` section, read its `map:`, `conventions:`, `gotchas:`, `workload:`, `growth:` instead.
3. **Understand the want.** One line before building: "You asked X. I take the goal to be Y. I will also do Z, and leave W." Y comes from the README, `purpose:`, `growth:`, nearby TODOs and recent commits. Z is the footprint of the last similar change: the commit that added the previous flag or endpoint, and every file it touched (tests, docs, help text, changelog, config). If the literal ask will not reach the goal (a longer timeout when the cause is a query per item), say so first.
4. **Think past the ask.** When the request adds a layer or a hard-to-undo choice (an API, queue, cache, auth, ORM, async, a new store), read `references/growth.md` in the skill folder: options from the project's evidence, the one that fits today, the seams that keep the others cheap.
5. **Build** under the rules below.
6. **Verify, then scout.** Run it. From the code you read, look for a measured slowdown on the path you touched, hand-rolled code the ladder covers, a bug next to the change, duplicated logic. Fix only what is inside the lines you change and trivially safe; list the rest under `Noticed:` (see below); never widen the diff silently.
7. **Offer what you learned.** If the task taught something non-obvious about the project, end with "Learned: ...; add to AGENTS.md?" and write it only on a yes.

## Never miss

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green. A test that contradicts the spec: leave it, finish the rest, report it.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom. Do not silence tools (`# type: ignore`, `# noqa`, `Any`, looser config).
- A request you cannot state as one change ("make the reports better") gets one to three short questions with suggested answers before any edit. A request that names the change is done, not discussed. A feature with several readings gets a one-page spec and its first slice (`workflow/specs-and-slices.md`).
- "Get rid of" a public name is a deprecation unless nothing outside this repository can use it (`workflow/deprecation-and-migration.md`).
- Do not hand-roll what the standard library or the community's standard library does well (an HTTP call with retries and pooling, dates, validation, argument parsing, retries): climb the ladder in `code/reuse.md` first, and say in the reply which rung you took and why.
- Every report ends with `Noticed:` and at most three lines from step 6, or `Noticed: nothing`.
- Smallest diff that solves it properly. A new dependency is chosen by the ladder and named in the reply (rung and reason), and needs a yes first when `ask-first:` says so. A public API change, a commit or a push only when asked.
- Use the project's own tools, runner and Python target, found from its lock file, `Makefile` or CI (`which-type.md`): never swap one, add a second for a job one does, or install silently. Commands in the leaves are written for uv; use the project's equivalent.
- Replies, comments and docs are short: what is not obvious, no filler. Never drop "not", "never", "only", "except".

## Read before you write

Read `code/smells.md` first, then only the leaf for the main thing the task does (a second only if clearly needed); others when you reach a situation they cover. `workflow/shipping.md` when about to report. Paths start at `development/`. Open each with Read; do not search.

- new function, class, option, constant, name: `code/minimalism.md`
- what exists for a job: `ecosystem.md`; hand-rolled utility, new package: `code/reuse.md`, `dependencies/dependencies.md`
- errors: `code/errors.md`; parsing input: `code/validation.md`; annotations: `code/typing.md`
- files, connections, locks, subprocesses, streams: `code/resources.md`
- feature newer than the Python target: `code/python-versions.md`; docstring, comment: `code/comments.md`
- logging, secrets, SQL, `eval`, `pickle`: `code/logging.md`, `code/security-basics.md`; script or CLI: `code/scripts.md`
- tests: `testing/testing.md`, `testing/smells.md`; slow code: `performance/index.md`
- retries, timeouts, circuit breakers: `application/shared/resilience.md`
- scope: `workflow/planning.md`; bug: `workflow/debugging.md`; restructuring: `workflow/refactoring.md`; unsure API: `workflow/checking-apis.md`; three or more outcomes, or "all"/"every": `workflow/gates.md` (a short list, then start); several readings: `workflow/specs-and-slices.md`; removing or replacing: `workflow/deprecation-and-migration.md`
- pattern, layers: `architecture/design-patterns.md`; data structure or algorithm: `architecture/fit.md`; design under real limits, `unsafe`: `architecture/senior-engineering.md`

The project's kind adds one index (`which-type.md` names it: library, service, worker, native). Read it and only it.
