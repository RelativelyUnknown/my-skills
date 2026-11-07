# Tooling notes

Situational choices for `setting-up-python-packages`. None is required.

- Run `vulture` occasionally to find dead code.
- Type checker: keep the detected one. Pyrefly (stable since 1.0) and ty (still a 0.0.x beta) are much faster than mypy and pyright; add one beside the existing checker only when asked, and never make a beta checker the only gate.
- Build backend: the template uses hatchling. `uv init` (uv 0.12+) generates `uv_build`, which suits pure-Python packages; keep it when present and give it an upper bound (`uv_build>=0.13,<0.14`) that you raise each uv minor release. Rust extensions use maturin.
- Hooks: when `.pre-commit-config.yaml` exists, `prek` runs the same file faster. Suggest it; do not switch unasked.
- Packages with C or Rust extensions can add a free-threaded job (`3.15t`) to CI; pure-Python packages need nothing extra.
- Hook scripts that block edits to tests and `pyproject.toml` also block adding new tests; set `ALLOW_TEST_EDITS=1` for sessions that write tests.
