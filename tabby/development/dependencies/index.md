# Dependencies

- uv, CI and Docker pages (`uv.md`, `uv-ci.md`, `uv-docker.md`): only when the project's runner is uv.
- dependencies.md: adding a package, a security alert, an audit.
- other runners (poetry, pdm, pipenv, hatch, pip): `dependencies.md` rules apply unchanged; use the runner's own commands and its lock file.
- uv.md: the runner is uv, or adding, locking, syncing, running scripts and tools.
- uv-ci.md: a CI job with uv.
- uv-docker.md: a Dockerfile with uv.
