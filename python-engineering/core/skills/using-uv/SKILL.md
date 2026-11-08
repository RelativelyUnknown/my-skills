---
name: using-uv
description: "Use when the runner is uv, or when adding dependencies, locking, syncing, running scripts or tools, or writing a Dockerfile or CI job with uv. Project, script, tool and pip modes, --locked versus --frozen, groups, pins, workspaces, image layering."
license: MIT
metadata:
  adapted-from: "wshobson/agents uv-package-manager (MIT, Seth Hobson); see SOURCE.md"
---

# Using uv

Defaults: read the `## Python defaults` section of AGENTS.md; infer what is missing from the repo; ask only what is still unknown, once; save the answers there. This skill applies when `runner=uv`; do not move a poetry, pdm or pip project to uv unasked. Commands below were run with uv 0.11.32 on 7 November 2026; uv changes quickly, so `uv help <command>` wins over this page.

## Pick the mode

- **Project** (`pyproject.toml` and `uv.lock`): `uv add`, `uv add --dev`, `uv remove`, `uv lock`, `uv sync`, `uv run`. Commit `uv.lock` and `.python-version`; never edit the lock by hand.
- **Script**: `uv add --script s.py pkg` writes a PEP 723 `# /// script` block, then `uv run s.py` builds the environment. A one-off dependency is `uv run --with rich s.py`.
- **Tool**: `uvx ruff check` runs a tool in a throwaway environment; `uv tool install ruff` installs a command-line tool for the user. Neither is a project dependency.
- **pip-compatible** (`uv pip install`): only for a project that is not a uv project. In a uv project, `uv pip install` bypasses the lock and the next `uv sync` removes the package.

## Rules

- Change dependencies with `uv add` and `uv remove`. If you edit `pyproject.toml` by hand, run `uv lock` after.
- Run commands with `uv run <cmd>`: it syncs first and needs no activation. A `VIRTUAL_ENV` that is not the project's is ignored with a warning; `--active` targets it.
- Dev tools go in a dependency group (`uv add --dev pytest` writes `[dependency-groups] dev`, PEP 735), not in an extra; extras are for users of the package. `uv sync` installs `dev` by default; `--no-dev`, `--group x`, `--only-group x`, `--extra x`, `--all-extras` change that.
- In CI and images use `uv sync --locked`: it fails when the lock is out of date with `pyproject.toml`. `--frozen` installs from the lock without checking it is current, so a stale lock is used silently. `uv lock --check` checks without installing. Then run with `uv run --no-sync`.
- Upgrade one package with `uv lock --upgrade-package name`, everything with `uv lock --upgrade`; `uv tree --outdated` shows what is behind. `uv lock --exclude-newer <date>` resolves as of a date.
- `uv python install 3.13` fetches an interpreter; `uv python pin 3.12` writes `.python-version`. `requires-python` is the support floor and the lock resolves for every version it allows, so keep it honest.
- A workspace is several packages with one lock. `uv init packages/x` inside a project registers the member in `[tool.uv.workspace]`; a sibling dependency is `name = { workspace = true }` under `[tool.uv.sources]`. Use `uv sync --package app` and `uv run --package app`.
- `uv sync --no-install-project` installs the dependencies but not the project: the dependency layer of a Docker image, built from `pyproject.toml` and `uv.lock` alone. Layering and a CI job: [references/ci-and-docker.md](references/ci-and-docker.md).
- `uv export --no-hashes --no-dev --format requirements-txt` produces a requirements file for tools that need one.
- `uv init --lib` writes the `uv_build` backend in 0.11; do not swap the backend of an existing project. Building, publishing and release checks belong to the library bundle, if installed.
- A private index is `[[tool.uv.index]]` with `explicit = true`, and a package taken from it is pinned under `[tool.uv.sources]`, so its name cannot be filled from the public index.
