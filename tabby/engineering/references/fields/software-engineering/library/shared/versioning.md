# Versioning

Built with uv 0.11.32 on 7 November 2026.

Pick one and read it everywhere else with `importlib.metadata.version("<dist-name>")`; never type the number twice.

- Static: `version = "2.0.0"` in `[project]` (`uv_build` and `hatchling` both build it). Bump it in the release commit.
- From a file: `dynamic = ["version"]` with `[tool.hatch.version]` and `path = "src/<pkg>/__init__.py"`; hatchling reads `__version__`. Built `0.4.0` from `__version__ = "0.4.0"`.
- From git tags: `requires = ["hatchling", "hatch-vcs"]`, `dynamic = ["version"]`, `[tool.hatch.version] source = "vcs"`, and optionally `[tool.hatch.build.hooks.vcs] version-file = "src/<pkg>/_version.py"` (git-ignored). A build at the tag `v1.2.3` gave `1.2.3`; one commit later it gave `1.2.4.dev1+g<sha>`.

Consequences to plan for:

- A version with a `+g<sha>` part is a local version, and PyPI rejects it. Publish only from a tagged commit, and make CI fetch the tags (a full clone, not a shallow one).
- `importlib.metadata.version(...)` reports the version recorded at install time. In an editable install it stayed `1.2.3` after a new commit until the package was reinstalled.
