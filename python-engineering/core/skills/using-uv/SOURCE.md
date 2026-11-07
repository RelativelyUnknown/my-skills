# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/uv-package-manager/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (345 lines) and advanced reference (473 lines) are mostly an installation and command tutorial. They are replaced by decision rules: which mode to use, lock discipline, groups, pins, workspaces and image layering.
- Each command and behaviour in the body was run with uv 0.11.32 on Python 3.12/3.13 in the container: `uv init --lib` (uv_build backend), `uv add --dev` writes `[dependency-groups]`, `uv sync --locked` fails on a stale lock while `--frozen` installs from it, `uv lock --check`, the `VIRTUAL_ENV` warning, `uv python pin`, `uv export`, `uv tree --outdated`, `uv add --script` and `uv run --with`, `uvx`, `uv init` inside a project registering a workspace member, `--package`, and `--no-install-project`. `uv pip install` inside a project is removed by the next `uv sync`.
- Not run here, taken from the uv documentation (raw files `docs/guides/integration/github.md` and `docker.md` on the main branch, read 7 November 2026): the private-index setting and the CI and Docker examples (`references/ci-and-docker.md`), including the pinned action SHAs and the `--no-install-workspace` and `--no-install-package` flags.
- Dropped: installation methods, the `pip` command table, the monorepo and cache-tuning sections, and the comparison with other tools.
