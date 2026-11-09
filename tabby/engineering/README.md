# engineering

A module of [Tabby](../SKILL.md): developing Python code and packages. It makes an AI agent write less slop: tests that can fail, errors that surface, fewer concepts, honest reports. Sources are credited in [`SOURCE.md`](SOURCE.md) and [`../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

## Layout

`index.md` is a front door of about 770 tokens: never-miss rules and a list of files to read. Everything else is read on demand from `references/`:

```
references/
  which-type.md                     signals -> kind paths, read once
  fields/
    software-engineering/
      all/          code/ testing/ performance/ dependencies/ workflow/   any Python project
      library/shared/  native/                                             packages others install; Rust or C behind Python
      application/  shared/ apis/{shared,http}/ workers/                   services and jobs
    software-architecture/                                                 patterns, boundaries
```

Every folder has an `index.md` with a "read when" line per file. Folders are added only when they have content; a missing path means no specialist guidance. `assets/` holds the `pyproject.toml`, `Makefile`, `ci.yml` and `release.yml` templates.

## Defaults

The skill reads a `## Python defaults` section of `AGENTS.md` (`kind`, `python`, `runner`, `types`, `layout`, `rigor`, `report`, `docstrings`), infers what is missing, asks once for the rest and saves the answers there. It takes no arguments.

## Evals

Cases are in `../evals/<case>/` (`prompt.md`, `case.yaml`, `graders/`, `fixture.sh`).

```bash
claude plugin eval tabby --scaffold --allow-tools Write Edit --judge-model sonnet --max-cost-usd 4
```

- `--scaffold` runs each case's `fixture.sh` as you; read it first.
- Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- A `tool_used: Skill` grader shows whether the skill fired on a plain request.
- `../evals/tabby.triggers.json` lists prompts that should and should not load the skill.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files for test-writing sessions.
- The skill runs no scripts; the few checks it needs are `grep` and `git` one-liners in the leaves.

## License

MIT. Adapted material keeps its upstream licence: `LICENSE.wshobson`.
