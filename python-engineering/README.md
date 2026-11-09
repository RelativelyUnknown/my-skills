# python-engineering

Part of the [skills repository](../README.md). One skill for developing Python code and packages, for GitHub Copilot first and any agent that reads `SKILL.md` folders. It makes an AI agent write less slop: tests that can fail, errors that surface, fewer concepts, honest reports. Sources are credited in [`SOURCE.md`](SOURCE.md) and [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

## Layout

`SKILL.md` is a front door of about 900 tokens: never-miss rules and a list of files to read. Everything else is read on demand from `references/`:

```
references/
  which-type.md                     signals -> kind paths, read once
  fields/
    software-engineering/
      all/          code/ testing/ performance/ dependencies/ workflow/   any Python project
      library/shared/                                                      packages others install
      application/  shared/ apis/{shared,http}/ workers/                   services and jobs
    software-architecture/                                                 patterns, boundaries
```

Every folder has an `index.md` with a "read when" line per file. Folders are added only when they have content; a missing path means no specialist guidance. `assets/` holds the `pyproject.toml`, `Makefile`, `ci.yml` and `release.yml` templates.

## Defaults

The skill reads a `## Python defaults` section of `AGENTS.md` (`kind`, `python`, `runner`, `types`, `layout`, `rigor`, `report`, `docstrings`), infers what is missing, asks once for the rest and saves the answers there. It takes no arguments.

## How routing was measured

Cases are in `evals/<case>/` (`prompt.md`, `case.yaml`, `graders/`, `fixture.sh`). The routed form was compared with the earlier 20 flat skills installed together, 26 cases, 3 runs per case, `claude plugin eval` with `--ablation none`:

| | 20 flat skills | routed (v2) |
| --- | --- | --- |
| mean score | 0.773 | 0.788 |
| cases where the skill never fired | 11 of 26 | 0 of 26 |
| cost per run | $0.090 | $0.102 |
| turns per run | 10.2 | 13.5 |

Six cases that missed a conditional read were then re-run with the v2.1 front door: their mean went from 0.61 to 0.78 (flat install: 0.85). The other 20 cases were not re-run on v2.1, and `optional-parquet-dependency` stayed low (0.26 against 0.69 flat) before one last row was added to the front door, which has not been measured. The routed form costs about 13% more per run than the flat install; its advantage is that the rules are loaded reliably. A first test, where each flat skill was chosen for its case, favoured flat (0.84 against 0.72) and was replaced by the all-installed comparison. Copilot was not run.

Application cases (10) and the pre-existing cases for the other leaves have baselines from earlier runs; the application and `python-review` cases were not part of this comparison.

```bash
claude plugin eval python-engineering --scaffold --allow-tools Write Edit --judge-model sonnet --max-cost-usd 4
```

- `--scaffold` runs each case's `fixture.sh` as you; read it first.
- Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- A `tool_used: Skill` grader shows whether the skill fired on a plain request.
- `evals/python-engineering.triggers.json` lists prompts that should and should not load the skill.

## Probed and not built

A leaf is written only where the model fails a case without it. These cases were run with and without the skill and the bare model passed, so no leaf exists for them:

- `native-gil-checksum`, `native-pyclass-by-value`, `native-free-threaded` (a Rust extension on PyO3 0.30.1: release the GIL with `detach`, extract a `#[pyclass]` by value after the 0.30 change, declare `gil_used = false`): 0.96, 1.0 and 1.0 without the skill. PyO3's changelog confirms the renames and removals these cases depend on (`allow_threads` to `detach` in 0.26, `from_py_object` opt-in from 0.27, the blanket `FromPyObject` for `Clone` pyclasses removed in 0.30). Still untested: wheel builds and CI for extensions, C-API reference counting, abi3 and stubs.
- `ml-leaky-validation` (a scikit-learn script with scaling fit on all rows, a shuffled split of weekly data and a store mean computed over all rows) and `de-rerunnable-load` (a nightly load that duplicates rows on re-run): 1.0 and 1.0 without the skill, three runs each. With the skill the leakage case scored 0.77 because my pipeline regex missed a different, valid fix; that is a grader miss, not a model failure.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files for test-writing sessions.
- The skill runs no scripts; the few checks it needs are `grep` and `git` one-liners in the leaves.

## License

MIT. Adapted material keeps its upstream licence: `LICENSE.wshobson`.
