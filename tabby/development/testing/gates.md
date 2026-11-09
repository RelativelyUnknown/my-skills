# Release-grade test gates

## Lowest-supported dependencies

A library declares lower bounds; test that they are true. One CI job runs `uv run --resolution lowest-direct pytest`, which installs the lowest compatible version of each direct dependency and the latest of everything else. If it fails, either raise the lower bound in `pyproject.toml` or fix the code. (`uv sync` accepts the same `--resolution` flag.)

## Installed-wheel test

Source-tree tests can pass while the built package is broken (missing data files, wrong includes). Test the artifact:

```bash
uv build --wheel -o /tmp/dist
uv venv /tmp/wheel-env
uv pip install --python /tmp/wheel-env/bin/python /tmp/dist/*.whl pytest
/tmp/wheel-env/bin/python -m pytest tests --import-mode=importlib -p no:cacheprovider
```

With the `src` layout and no `pythonpath` setting, the tests import the installed wheel. If the project sets `pythonpath = ["src"]`, run this from a copy of `tests/` outside the repo.

## Coverage gate

Branch coverage with a floor that only ratchets up: `--cov=<pkg> --cov-branch --cov-fail-under=<current-floor>`. Raise the floor when coverage rises. Lower it only with a stated reason.
