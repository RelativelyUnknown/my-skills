---
name: setting-up-python-packages
description: "Scaffolds or audits a Python package: src layout, pyproject.toml, uv, ruff, mypy, pytest config, py.typed, one check command, CI workflow. Use when creating a new package, or editing build, lint, type-check, dependency or CI configuration."
argument-hint: "[python=3.12 runner=uv types=mypy layout=src backend=hatchling]"
---

# Setting up Python packages

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root. It prints the project's facts (`python.target`, `runner`, `layout`, `backend`, `lint`, `types`, `ci`, `tools.missing`, ...); `# default` means nothing was found.

- Arguments (`key=value` after the skill name) override detected facts: argument, then detected, then default.
- **Existing project: keep its tools.** Poetry, black, flake8, pyright, setuptools stay. Do the task with them, report what differs from the defaults below as a suggestion, and migrate only if asked. Do not edit CI, lint or pytest config beyond what the task needs.
- **New project: use the defaults** (uv, hatchling, ruff, mypy strict, pytest, `src` layout) from the templates in `assets/`.
- Report `tools.missing`; never install a tool or dependency silently.

## New package checklist

1. `pyproject.toml` is the only config file: no `setup.py`, `setup.cfg` or `requirements*.txt`. Start from [assets/pyproject.toml](assets/pyproject.toml); replace the `<placeholders>` and set the Python versions from `python.target`. `requires-python` has a lower bound only.
2. `src/<pkg>/__init__.py` with `__all__`, an empty `src/<pkg>/py.typed`, and `tests/` mirroring the package (see `testing-python-packages`).
3. One command runs lint, type check and tests, locally and in CI: copy [assets/Makefile](assets/Makefile) (`make check`), or the equivalent for the project's runner.
4. CI: copy [assets/ci.yml](assets/ci.yml). It tests `python.target` and the newest release, installs from the lock file, runs only `make check`, grants `contents: read`, and uses no secrets. Pin each action to its latest release tag (`git ls-remote --tags https://github.com/<owner>/<action>`).
5. Dev tools are pinned by the lock file (`uv sync --locked`). Keep runtime dependencies minimal; heavy or niche ones go in extras.
6. The test suite runs with no network, no secrets and no running services.
7. `.gitignore` covers `.venv/`, `__pycache__/`, `dist/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`.

Run `make check` on the result and show its output. A scaffold you did not run is not done.

## Layout

Packages are organized by component; dependencies point one way. Look at the tree before adding a file.

- Name packages for what they own (`billing/`, `ingest/`, `auth/`), never for the shape of the code (`models/`, `utils/`, `common/`, `misc/`, `base/`).
- A component is a subpackage with its own `__init__.py` and tests that mirror it. Nest only when a package has distinct components, to about three levels below the source root.
- Each package has a public face: its `__init__.py` re-exports what others may use, and other packages import from it, not from internal modules. Layers point one way (`api` to `services` to `domain`); a circular import means the boundary is in the wrong place, so move the boundary instead of hiding the import inside a function.
- Shared types live in a leaf package that imports nothing internal.
- One primary concept per module. Name files for their contents, without repeating the package name. A module past a few hundred lines is a signal to split by concept.
- **Each fact has one home**: the version, the dependency list, a schema, a default config value. Other files read or link to it. The version lives in `pyproject.toml`; code that needs it uses `importlib.metadata.version("<pkg>")` instead of a second literal.
- Give each kind of content one home: docstrings for API behavior, the README for install and usage, `docs/` for concepts, commit messages for history, config comments for config.
- Never hand-edit generated files; edit the source and regenerate. A new top-level directory needs a reason. Update an architecture file if one exists; do not create one unasked.

## Tooling notes

- Mechanical rules live in tool config, not in prose: the ruff list in the template covers bare and blind `except`, mutable defaults, positional booleans, `Any`, leftover `print`, f-strings in logging, blocking calls in async code and more. Do not select ruff's `D1xx` rules; they push filler docstrings.
- `strict = true` in `[tool.pytest.ini_options]` needs pytest 9; on older pytest use `--strict-markers` and `xfail_strict = true`.
- `make complexity` runs `xenon` as advice only and is not part of `check`. Read its ranks as hints; do not contort code to reach an A, and do not add it as a CI gate unless asked.
- Run `vulture` occasionally to find dead code.
- Type checker: keep the detected one. Pyrefly (stable since 1.0) and ty (still a 0.0.x beta) are much faster than mypy and pyright; add one beside the existing checker only when asked, and never make a beta checker the only gate.
- Build backend: the template uses hatchling. `uv init` (uv 0.12+) generates `uv_build`, which suits pure-Python packages; keep it when present and give it an upper bound (`uv_build>=0.13,<0.14`) that you raise each uv minor release. Rust extensions use maturin.
- Hooks: when `.pre-commit-config.yaml` exists, `prek` runs the same file faster. Suggest it; do not switch unasked.
- Packages with C or Rust extensions can add a free-threaded job (`3.15t`) to CI; pure-Python packages need nothing extra.
- Hook scripts that block edits to tests and `pyproject.toml` also block adding new tests; set `ALLOW_TEST_EDITS=1` for sessions that write tests.
