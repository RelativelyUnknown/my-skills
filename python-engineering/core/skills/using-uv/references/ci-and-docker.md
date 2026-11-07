# uv in CI and Docker

From the uv documentation (integration guides for GitHub Actions and Docker), checked 7 November 2026. Not run here: the container has no Docker, and CI needs a hosted runner.

## GitHub Actions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
        with:
          version: "0.13.7"  # pin uv; the commands in this skill were run with 0.11.32
      - run: uv sync --locked
      - run: uv run --no-sync pytest
```

The uv guide pins both actions to commit SHAs, as above; this repository's advice is a tag or a SHA (see `auditing-python-dependencies`). The guide installs Python with `uv python install`; `setup-uv` and `actions/setup-python` also work.

## Docker: dependencies first, source second

```dockerfile
FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# The dependency layer changes only when pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project --no-dev

COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

CMD ["uv", "run", "--no-sync", "python", "-m", "app"]
```

- Pin the uv image to a version, not `latest`. The uv guide mounts only `uv.lock` for the dependency layer and uses `--frozen` there, because `pyproject.toml` is not copied yet; copying both files first, as above, lets `--locked` check the lock in that layer too.
- In a workspace, `--no-install-workspace` leaves out the project and every workspace member from the dependency layer; `--no-install-package <name>` leaves out one package.
- `UV_LINK_MODE=copy` avoids hard-link warnings when the cache is a mounted volume; `UV_COMPILE_BYTECODE=1` trades build time for start-up time.
- A multi-stage build copies `/app/.venv` from the build stage into a slim runtime stage and puts `.venv/bin` on `PATH`.
- Run as a non-root user; secrets never go in `COPY` or `ENV` (the application bundle's deployment notes cover this, if installed).
