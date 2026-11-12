# Which kind of project, and which tools

Read once per project. Save the matching paths, comma-separated, as `kind:` in the `## Tabby` section of AGENTS.md. Paths are under `development/`; the core skill lists the leaves for each kind. A path with no folder is not built: use `code` and say so.

- `[project]` with a build backend and `src/`; others import it: `library/shared`
- `[project]` plus `Cargo.toml` (maturin), `ext_modules`, `CMakeLists.txt`, `meson.build` or `.pyx` files: `library/native`
- FastAPI, Django REST, Flask JSON or similar HTTP service: `application/apis/http`
- A queue client, worker or scheduler: `application/workers`
- Async handlers, caches, other service code: `application/shared`
- A question about boundaries, patterns, layers or extension points: `architecture`
- Anything else, or unsure: `code`

## Which tools the project uses

The project's tools win, whatever Tabby's own templates default to. A team on poetry stays on poetry, one on black stays on black, one on unittest keeps writing unittest. Read the stack from the repo before the first command, and put every command through the project's runner.

| Fact | Where it shows |
| --- | --- |
| Runner and lock | `uv.lock` (uv); `poetry.lock` or `[tool.poetry]` (poetry); `pdm.lock` (pdm); `Pipfile` (pipenv); `[tool.hatch.envs]` (hatch); `pixi.toml` (pixi); `environment.yml` (conda); `requirements*.txt` only (pip) |
| Build backend | `build-backend` in `[build-system]`: `hatchling`, `setuptools.build_meta`, `poetry.core.masonry.api`, `pdm.backend`, `flit_core`, `maturin`, `scikit_build_core`, `mesonpy` |
| Tests | `[tool.pytest.ini_options]`, `pytest.ini` or `conftest.py` (pytest); `unittest.TestCase` in existing tests (unittest); `tox.ini` or `noxfile.py` (the entry point that runs them) |
| Format and lint | `[tool.ruff]` or `ruff.toml`; `[tool.black]`; `.flake8` or `[flake8]` in `setup.cfg`; `[tool.isort]`; `.pylintrc`; `.pre-commit-config.yaml` |
| Types | `[tool.mypy]` or `mypy.ini`; `pyrightconfig.json` or `[tool.pyright]`; pyrefly, ty |
| The check command | the `check`, `test` or `ci` target in `Makefile` or `justfile`; `tox` or `nox` sessions; the steps in `.github/workflows/` or `.gitlab-ci.yml` |
| Docs | `mkdocs.yml` (MkDocs); `docs/conf.py` (Sphinx) |

Rules:

- Run commands as the project does: `poetry run pytest`, `pdm run`, `hatch run`, `pipenv run`, `uv run`, or `python -m` inside its environment. Find the form in the `Makefile`, CI file or the runner's `--help`; do not translate a command from another tool from memory.
- Do not add a second tool for a job one already does (a ruff config beside black and flake8, a `uv.lock` beside `poetry.lock`, pytest beside unittest), and do not migrate unasked.
- The templates in `development/assets/` and `dependencies/uv*.md` are for a new project whose owner has not chosen a stack, or who chose that one. Otherwise adapt the idea to the stack in use.
- If the project's tool is missing from the machine, say so and ask; do not substitute another and do not install one unasked.
- Two stacks in one repo (a `poetry.lock` and a `uv.lock`, two linters): report the conflict and ask which is current.
