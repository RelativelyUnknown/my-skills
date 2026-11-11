# Research the project (read-only)

Build the evidence table the interview starts from. Breadth first: a handful of commands per facet, depth only where an answer needs it. Start from entry points, not from imports. If you can run subagents, the facets are independent and can run in parallel; otherwise do them in order. Return only facts that have a source.

## Facets

1. **What it is and how it runs.** Entry points: `[project.scripts]` and entry-point groups in `pyproject.toml`, `__main__.py`, `if __name__`, framework apps (`FastAPI(`, `Flask(`, `Django` settings), worker definitions. Build and check commands as written in `Makefile`, `noxfile.py`, `pyproject.toml` and `.github/workflows/`: read them, do not run them.
2. **Users and surface.** What others touch: names exported in `__init__.py` and `__all__`, HTTP routes, CLI commands, config keys. What the README claims the project is for. Name each job by what it does for someone, not by the technology.
3. **Native code.** `Cargo.toml`, `setup.py` with `ext_modules`, `CMakeLists.txt`, `meson.build`, `*.pyx`, `*.c`, `*.rs`. Which functions cross into Python and what calls them.
4. **How data is reached, and the quality gates and tool stack.** For data: plain SQL, a query builder or an ORM, how many entities, whether the driver is sync or async. For the rest: Where tests live and how they are named, test count, CI jobs, linters, type checker, coverage settings, pre-commit hooks, and the runner, build backend, test framework and formatter (the table in `../tabby/development/which-type.md`). The stack is a fact to record, not a question to ask.
5. **History and decisions.** `git log --oneline | wc -l`, first and last commit dates, the files changed most in six months (`git log --since=6.months --name-only --pretty=format: | sort | uniq -c | sort -rn | head`), `docs/adr/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, open `TODO` and `FIXME` comments.
6. **Agent files.** `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules`. Merge their useful lines into AGENTS.md; do not duplicate.

## The evidence table

| Fact | Source | Status |
| --- | --- | --- |
| Rust extension, one exported function `crc` | `src/lib.rs:4`, `Cargo.toml:6` | seen |
| Check command is `make check` | `Makefile:2`, `.github/workflows/ci.yml:8` | seen |
| Library others install | `pyproject.toml:1` (`[project]`), `python/fastsum/__init__.py:3` | inferred |
| Who uses it, success, growth, limits | none | needs you |

- `seen`: the source states it. `inferred`: you concluded it from sources; say so and let the user correct it. `needs you`: code cannot answer.
- Where docs and code disagree, record both sides with their sources and ask which is true.
- Where a purpose is not clear from the code, derive a label from the file name, mark it `review` and ask.

## Project state

Count from the table: code files, commits, tests, CI jobs, docs. Choose New, Young or Established using the table in `start.md`. An empty folder is New and has nothing to research: go straight to the questions.
