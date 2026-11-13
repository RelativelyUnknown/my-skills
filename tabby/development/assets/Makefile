.DEFAULT_GOAL := help
.PHONY: help check lint fix types test complexity

help: ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

# The one command: run it locally and in CI.
check: lint types test ## Lint, type check and test (what CI runs)

lint: ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

fix: ## Apply formatting and safe lint fixes
	uv run ruff check --fix .
	uv run ruff format .

types: ## Type check
	uv run mypy src tests

# `make test` runs everything; `make test T=tests/test_orders.py::test_refund` runs one test while you work.
test: ## Run the tests (one test: make test T=path::name)
	uv run pytest $(T)

# Advisory only, not part of `check`. Read the ranks as hints about hard-to-follow code;
# do not contort code to reach an A. Needs xenon in the dev group.
complexity: ## Advisory complexity ranks (not part of check)
	-uv run xenon --max-absolute B --max-modules B --max-average A src
