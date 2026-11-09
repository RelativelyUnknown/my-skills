# Start: new project or existing project

Goal: a short `## Tabby` section in AGENTS.md that every later task can read in a few hundred tokens.

## 1. Look first (no questions yet)

With grep and `ls`, not scripts. Note each finding as `(inferred)`.

- `pyproject.toml` (`[project]`, build backend, `requires-python`, `[tool.*]`), lockfile (`uv.lock`, `poetry.lock`), `Makefile`, `noxfile.py`, `.github/workflows/`.
- Native code: `Cargo.toml` (maturin, PyO3), `setup.py` with `ext_modules`, `CMakeLists.txt`, `meson.build`, `*.pyx`, `*.c`, `*.rs` under `src/`.
- Kind: `[project]` plus `src/` and a build backend means a library; FastAPI, Django, Flask imports mean an HTTP service; celery, rq, arq imports mean workers; `data/`, notebooks, `dbt_project.yml` mean data or ML.
- Docs and decisions: `docs/`, `mkdocs.yml`, `docs/conf.py`, `docs/adr/`, `CONTRIBUTING.md`, `CHANGELOG.md`, `SECURITY.md`.
- Existing agent files: AGENTS.md, CLAUDE.md, `.github/copilot-instructions.md`. Merge into AGENTS.md; do not duplicate.
- An empty folder means a fresh project: nothing to infer.

## 2. Ask (three questions, one round)

Use your question tool if you have one: one call, three questions, a recommended option first on each. Without one, send one short message with the same three. Skip a question the repo already answers well, and say what you inferred instead.

1. **What is it, and who uses it?** Library others install, HTTP service, worker or pipeline, command-line tool, internal script, data or ML project.
2. **What is likely to change next year?** Pick any: more users or scale, a hot path in Rust or C, a public API others depend on, new integrations or data sources, a second deployment target, nothing big.
3. **What is off limits?** Out of scope, things not to touch, hard constraints (Python versions, platforms, no new dependencies, stable API, data that must not change). Free text is fine.

Ask a follow-up only when an answer changes what you would build: "a hot path in Rust" needs to know which function and what speed-up would count; "public API" needs to know who depends on it today.

## 3. Restate, get a yes, save

Write six lines back, in the user's words where possible:

```
Outcome:      <what it does and for whom>
Success:      <how we will know in six months>
Growth:       <ordered expected changes>
Constraints:  <versions, platforms, rules>
Out of scope: <what we are not doing>
Skills:       python-engineering, python-review[, python-design]; kind: <path>
```

"Sounds good" or "whatever you think" is not a yes: ask what to refine. On a clear yes, write the section and stop; do not start work in the same turn.

## 4. The section

```markdown
## Tabby
reviewed: 2026-11-09
purpose: one line
users: who, in what situation
goals: up to three, measurable where possible
growth: ordered list; the first item is likeliest
out-of-scope: list
constraints: python 3.12+; no new runtime dependencies without asking
kind: software-engineering/library/native
skills: python-engineering, python-review
docs: README, reference, ADR
commands: one canonical check command, e.g. `nox -e local` or `make check`
```

- `kind:` is one of these paths (more in `python-engineering/references/which-type.md`):
  - library others install: `software-engineering/library/shared`
  - library with Rust, C or Cython behind a Python API: `software-engineering/library/native`
  - HTTP service: `software-engineering/application/apis/http`
  - queue worker or scheduler: `software-engineering/application/workers`
  - anything else: `software-engineering/all` `docs:` lists the page types to keep current (see `python-engineering/references/fields/documentation/index.md`): a library usually gets README, reference, how-to, changelog; a service gets README, runbook, ADR.
- Add `python-design` to `skills:` only when the user wants diagrams or explainers.
- Keep `## Python defaults` as it is; Tabby does not replace it.
- No user to ask (CI, or the user says they cannot answer now)? Do not ask and do not stop: write the section from the repo, mark every unknown `(assumed)`, and tell the user which entries need confirming.

## 5. Staleness

Answers go stale. Each time a task conflicts with the section, ask once whether it still fits, then edit the section and its `reviewed:` date.
