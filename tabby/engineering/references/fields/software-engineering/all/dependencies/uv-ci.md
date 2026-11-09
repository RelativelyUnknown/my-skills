# uv in CI

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
          version: "0.13.7"  # pin uv; the commands here were run with 0.11.32
      - run: uv sync --locked
      - run: uv run --no-sync pytest
```

The uv guide pins both actions to commit SHAs, as above; this repository's advice is a tag or a SHA (see [dependencies.md](dependencies.md)). The guide installs Python with `uv python install`; `setup-uv` and `actions/setup-python` also work.
