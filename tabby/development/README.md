# development

A module of [Tabby](../SKILL.md) for writing, testing, packaging and running Python: errors that surface, fewer concepts, tests that can fail, honest reports, and Rust or C behind a Python API. Sources are credited in [`SOURCE.md`](SOURCE.md) and [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

**Entry point:** [`index.md`](index.md), about 850 tokens: the never-miss rules and the list of files to read for each kind of task. Everything else loads on demand.

## Layout

```
index.md                  front door
which-type.md             project signals -> kind paths
code/                     any Python project: smells, errors, typing, resources, minimalism, stdlib first
testing/                  tests that can fail; mocking, fixtures, rigor (property-based, mutation, release gates)
performance/              measure first, then fix in order of leverage (one file)
dependencies/             uv, CI, Docker, choosing and vetting packages
workflow/                 planning, debugging, refactoring, checking APIs, shipping
library/                  packages others install
  shared/                 API design, package setup, layout, versions, release
  native/                 Rust or C behind a Python API: architecture, PyO3, the C API, wheels and CI
application/              services and jobs
  shared/                 async, observability, configuration, resilience, persistence, deployment
  apis/                   shared/ and http/
  workers/                background jobs
architecture/             patterns, layers, extension points; design fit (choosing data structures and representations)
assets/                   pyproject.toml, Makefile, ci.yml, release.yml; native/ (Cargo lints, nanobind CMake and pyproject)
```

Every area has an `index.md` with a "read when" line per file, and most have a `smells.md`: a list of mistakes for that area, each line a smell and its fix (`code/`, `testing/`, `library/`, `library/native/`, `application/`). A path with no folder means no specialist guidance exists for it.

## Defaults

Reads the `## Python defaults` section of `AGENTS.md` (`python`, `runner`, `types`, `layout`, `rigor`, `report`, `docstrings`), infers what is missing, asks once for the rest and saves the answers there. It takes no arguments.

## Evals

The development cases are in [`../evals/`](../evals/) (errors, dependencies, typing, services, workers, native extensions, ML and data pipelines). Run them from the repository root:

```bash
claude plugin eval tabby --scaffold --allow-tools Write Edit --judge-model sonnet --max-cost-usd 4
```

- `--scaffold` runs each case's `fixture.sh` as you; read it first.
- Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- A `tool_used: Skill` grader shows whether the skill fired on a plain request.
- [`../evals/tabby.triggers.json`](../evals/tabby.triggers.json) lists prompts that should and should not load the skill.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files for test-writing sessions.
- No scripts: the few checks it needs are `grep` and `git` one-liners in the leaves.

## Licence

MIT. Adapted third-party material keeps its upstream licence: [`LICENSE.wshobson`](LICENSE.wshobson).
