.PHONY: check lint types test complexity

# The one command: run it locally and in CI.
check: lint types test

lint:
	uv run ruff check .
	uv run ruff format --check .   # fix with: uv run ruff format .

types:
	uv run mypy src tests

test:
	uv run pytest

# Advisory only, not part of `check`. Read the ranks as hints about hard-to-follow code;
# do not contort code to reach an A. Needs xenon in the dev group.
complexity:
	-uv run xenon --max-absolute B --max-modules B --max-average A src
