# Package setup

## Start

- **Existing project: keep its tools.** Poetry, black, flake8, pyright, setuptools stay. Do the task with them, report what differs from the defaults below as a suggestion, and migrate only if asked. Do not edit CI, lint or pytest config beyond what the task needs.
- **New project: use the defaults** (uv, hatchling, ruff, mypy strict, pytest, `src` layout) from the templates in `assets/`.
- Never install a tool or dependency silently.

## New package checklist

1. `pyproject.toml` is the only config file: no `setup.py`, `setup.cfg` or `requirements*.txt`. Start from `assets/pyproject.toml`; replace the `<placeholders>` and set the Python versions from the Python target. `requires-python` has a lower bound only.
2. `src/<pkg>/__init__.py` with `__all__`, an empty `src/<pkg>/py.typed`, and `tests/` mirroring the package ([testing.md](../../testing/testing.md)).
3. One command runs lint, type check and tests, locally and in CI: copy `assets/Makefile` (`make check`), or the equivalent for the project's runner.
4. CI: copy `assets/ci.yml`. It tests the Python target and the newest release, installs from the lock file, runs only `make check`, grants `contents: read`, and uses no secrets. Pin each action to its latest release tag (`git ls-remote --tags https://github.com/<owner>/<action>`).
5. Dev tools are pinned by the lock file (`uv sync --locked`). Keep runtime dependencies minimal; heavy or niche ones go in extras.
6. The test suite runs with no network, no secrets and no running services.
7. `.gitignore` covers `.venv/`, `__pycache__/`, `dist/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`.

Run `make check` on the result and show its output. A scaffold you did not run is not done.
