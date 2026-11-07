# Versions and entry points

Where the version lives, how a command gets onto the user's path, and how to choose a build backend. Everything here was built with uv 0.11.32 on 7 November 2026.

## Contents

- One source for the version
- Entry points
- Choosing a build backend

## One source for the version

Pick one and read it everywhere else with `importlib.metadata.version("<dist-name>")`; never type the number twice.

- Static: `version = "2.0.0"` in `[project]` (`uv_build` and `hatchling` both build it). Bump it in the release commit.
- From a file: `dynamic = ["version"]` with `[tool.hatch.version]` and `path = "src/<pkg>/__init__.py"`; hatchling reads `__version__`. Built `0.4.0` from `__version__ = "0.4.0"`.
- From git tags: `requires = ["hatchling", "hatch-vcs"]`, `dynamic = ["version"]`, `[tool.hatch.version] source = "vcs"`, and optionally `[tool.hatch.build.hooks.vcs] version-file = "src/<pkg>/_version.py"` (git-ignored). A build at the tag `v1.2.3` gave `1.2.3`; one commit later it gave `1.2.4.dev1+g<sha>`.

Consequences to plan for:

- A version with a `+g<sha>` part is a local version, and PyPI rejects it. Publish only from a tagged commit, and make CI fetch the tags (a full clone, not a shallow one).
- `importlib.metadata.version(...)` reports the version recorded at install time. In an editable install it stayed `1.2.3` after a new commit until the package was reinstalled.

## Entry points

A command is `[project.scripts]` with `name = "pkg.cli:main"`. `main()` returns `None` or an exit code; the generated script calls `sys.exit(main())`. After `uv sync`, `uv run name` works, and the wheel's `entry_points.txt` lists it under `[console_scripts]`. Check it in the built wheel, not in the source tree (`unzip -p dist/*.whl '*/entry_points.txt'`).

## Choosing a build backend

Keep the one the project has. For a new pure-Python package: `uv_build` (what `uv init --package` and `--lib` write) when nothing special is needed; `hatchling` for tag-based versions, build hooks or file selection; `setuptools` for an existing setup that already uses it; `flit-core` for a single module. Extension modules use `maturin`, `scikit-build-core` or `meson-python` (the native-extension bundle covers them, if installed). Give `uv_build` the upper bound uv writes (`uv_build>=0.11.32,<0.12.0`) and raise it each uv minor release.
