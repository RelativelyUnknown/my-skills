# Source

`references/versions-and-entry-points.md` is adapted from two upstream skills. The rest of this skill is original to this repository.

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-packaging/` and `plugins/python-development/skills/python-project-structure/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream licence is kept as `LICENSE.wshobson` and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- `python-packaging` (166 + 717 lines): the src layout, minimal `pyproject.toml`, publishing to PyPI and the GitHub Actions workflow are already covered here and in `releasing-python-packages` (trusted publishing, wheel smoke test), so they are not copied. Folded in, rewritten and rebuilt: dynamic versioning and console-script entry points. Built with uv 0.11.32: hatchling reading `__version__` from a file (0.4.0), hatch-vcs from a tag (1.2.3, then `1.2.4.dev1+g<sha>` one commit later, a local version PyPI rejects), a static `uv_build` version (2.0.0), `[project.scripts]` appearing in the wheel's `entry_points.txt` and running with `uv run`, and the installed metadata staying at the old version until reinstall. The upstream setuptools-scm example and the Click and argparse listings are dropped.
- `python-project-structure` (252 lines): one concept per file, explicit `__all__`, flat hierarchies and mirrored test files are already rules here and in `designing-package-apis`. The layered-architecture and domain-driven structures are not folded in: they add layers this repository's rules decline until they are needed.
- Corrected in this skill while verifying: `references/tooling-notes.md` said `uv init` (uv 0.12+) writes `uv_build`; with uv 0.11.32 `uv init --package` and `--lib` already do, and plain `uv init` writes an application with no build system.
