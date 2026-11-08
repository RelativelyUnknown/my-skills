---
name: python-engineering
description: "Rules for every Python code change: error handling, minimalism, standard library first, typing, tests, dependencies, performance, packaging, and the end-of-task report. Use whenever you write, modify, refactor, debug, test, speed up or release Python code; load it before editing any .py file."
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

## Route

1. Any code change: read `references/fields/software-engineering/all/index.md`, then the `index.md` of the folder that matches the task.
2. Project kind: for each path in `kind`, read `references/fields/<path>/index.md`. No `kind`: read `references/which-type.md` once and save the path(s).
3. A path with no folder: use `software-engineering/all` and say no specialist guidance exists.
