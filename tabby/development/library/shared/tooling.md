# Tooling

A rule a tool can check should be checked by the tool, not remembered by an agent or reader. Ask: is this mechanical? Then it goes in config and CI; prose is for judgment. A tool's score is a hint to look at the code, never a target to game.

- Mechanical rules live in tool config, not in prose: the ruff list in the template covers bare and blind `except`, mutable defaults, positional booleans, `Any`, leftover `print`, f-strings in logging, blocking calls in async code and more. Do not select ruff's `D1xx` rules; they push filler docstrings.
- Formatting is checked, not argued: the template's `make lint` runs `ruff format --check .` after `ruff check .`, so an unformatted file fails `make check`. A project that already formats with black keeps black. Ruff exits with an error on an unknown rule code in `[tool.ruff]`, so a typo in the template's list shows up the first time it runs. Nothing in the template validates the rest of `pyproject.toml`; `uv build` and `uvx twine check dist/*` ([release.md](release.md)) catch metadata errors at release, and PyPA's `validate-pyproject` can check the file against the schema (not run here).
- `strict = true` in `[tool.pytest.ini_options]` needs pytest 9; on older pytest use `--strict-markers` and `xfail_strict = true`.
- `make complexity` runs `xenon` as advice only and is not part of `check`. A rank (`xenon`, `radon cc`, a lint rule) is a hint, not a verdict: simplify when you can say what is hard to follow and a clearer shape exists (early returns, a lookup table). Do not contort logic or split a function into vaguely named fragments to reach an A; a flat run of cases or a parser table that ranks C stays as it is, and the report says so. Never add `# noqa`, raise a threshold or make a test pass differently because of a rank; if CI gates on it and fails, report the failure and the readable options.

- Run `vulture` occasionally to find dead code.
- Type checker: keep the detected one. Pyrefly (stable since 1.0) and ty (still a 0.0.x beta) are much faster than mypy and pyright; add one beside the existing checker only when asked, and never make a beta checker the only gate.
- Build backend: the template uses hatchling. `uv init --package` and `--lib` write `uv_build` (checked with uv 0.11.32; plain `uv init` makes an application with no build system), which suits pure-Python packages; keep it when present and give it the upper bound uv writes (`uv_build>=0.11.32,<0.12.0`), raised each uv minor release. Rust extensions use maturin. Backend choice is below; versions and entry points: [versioning.md](versioning.md), [entry-points.md](entry-points.md).
- Hooks: when `.pre-commit-config.yaml` exists, `prek` runs the same file faster. Suggest it; do not switch unasked.
- Packages with C or Rust extensions can add a free-threaded job (`3.15t`) to CI; pure-Python packages need nothing extra.
- Hook scripts that block edits to tests and `pyproject.toml` also block adding new tests; set `ALLOW_TEST_EDITS=1` for sessions that write tests.

## Choosing a build backend

Keep the one the project has. For a new pure-Python package: `uv_build` (what `uv init --package` and `--lib` write) when nothing special is needed; `hatchling` for tag-based versions, build hooks or file selection; `setuptools` for an existing setup that already uses it; `flit-core` for a single module. Extension modules use `maturin`, `scikit-build-core` or `meson-python`. Give `uv_build` the upper bound uv writes (`uv_build>=0.11.32,<0.12.0`) and raise it each uv minor release.
