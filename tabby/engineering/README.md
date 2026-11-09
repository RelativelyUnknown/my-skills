# engineering

A module of [Tabby](../SKILL.md) for writing, testing, packaging and running Python: errors that surface, fewer concepts, tests that can fail, honest reports, and Rust or C behind a Python API. Sources are credited in [`SOURCE.md`](SOURCE.md) and [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

**Entry point:** [`index.md`](index.md), about 850 tokens: the never-miss rules and the list of files to read for each kind of task. Everything else loads on demand.

## Layout

```
index.md                              front door
references/
  which-type.md                       project signals -> kind paths
  fields/
    software-engineering/
      all/            code/ testing/ performance/ dependencies/ workflow/    any Python project
      library/        shared/ native/                                        packages others install; Rust or C behind Python
      application/    shared/ apis/{shared,http}/ workers/                   services and jobs
    software-architecture/                                                   patterns, layers, extension points
assets/                               pyproject.toml, Makefile, ci.yml, release.yml templates
```

Every folder has an `index.md` with a "read when" line per file. A path with no folder means no specialist guidance exists for it.

## Defaults

Reads the `## Python defaults` section of `AGENTS.md` (`kind`, `python`, `runner`, `types`, `layout`, `rigor`, `report`, `docstrings`), infers what is missing, asks once for the rest and saves the answers there. It takes no arguments.

## Evals

The engineering cases are in [`../evals/`](../evals/) (errors, dependencies, typing, services, workers, native extensions, ML and data pipelines). Run them from the repository root:

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
