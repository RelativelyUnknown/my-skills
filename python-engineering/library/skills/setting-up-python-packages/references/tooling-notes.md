# Tooling notes

Situational choices for `setting-up-python-packages`. None is required.

- Run `vulture` occasionally to find dead code.
- Type checker: keep the detected one. Pyrefly (stable since 1.0) and ty (still a 0.0.x beta) are much faster than mypy and pyright; add one beside the existing checker only when asked, and never make a beta checker the only gate.
- Build backend: the template uses hatchling. `uv init --package` and `--lib` write `uv_build` (checked with uv 0.11.32; plain `uv init` makes an application with no build system), which suits pure-Python packages; keep it when present and give it the upper bound uv writes (`uv_build>=0.11.32,<0.12.0`), raised each uv minor release. Rust extensions use maturin. Versions, entry points and the choice of backend: [versions-and-entry-points.md](versions-and-entry-points.md).
- Hooks: when `.pre-commit-config.yaml` exists, `prek` runs the same file faster. Suggest it; do not switch unasked.
- Packages with C or Rust extensions can add a free-threaded job (`3.15t`) to CI; pure-Python packages need nothing extra.
- Hook scripts that block edits to tests and `pyproject.toml` also block adding new tests; set `ALLOW_TEST_EDITS=1` for sessions that write tests.
