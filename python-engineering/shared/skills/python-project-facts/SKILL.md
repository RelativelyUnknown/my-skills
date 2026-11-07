---
name: python-project-facts
description: "Detects a Python project's version, runner, layout, tools and kind (library, application, native extension, data pipeline, ML, script and more) and says which skill bundles fit. The other python skills run its script; install it with them."
argument-hint: "[kind=library]"
---

# Python project facts

The other python skills run `scripts/detect_project.py` before they act, so they follow the project's real tools and versions instead of guessing. Install this skill in the same folder as them.

## Run it

`python3 <this skill's folder>/scripts/detect_project.py [kind=<kind>] [project root]`, from the project root. Standard library only, Python 3.11+. Each line is `key=value  # where it was found`; `# default` means nothing was found, so the value is an assumption.

## Read the output

- `python.target`, `runner`, `layout`, `backend`, `test`, `types`, `lint`, `async`, `ci`: the project's real choices. Keep them; never add a second tool for the same job.
- `tools.missing`: tools the project declares that this machine lacks. Report them; never install silently.
- `kind`: what the project is, from its files and dependencies. `kinds` lists every match and `kind` is the most specific. If it is wrong, run again with `kind=<kind>`.
- `bundles`: the skill bundles that fit (`core` always). `bundles.missing`: recommended skills that are not installed, as `bundle[skill,...]`. If it is neither `none` nor `unknown`, tell the user once which skills to install.

## Kinds and bundles

- `library`: a package with a build backend. Bundle `library`.
- `application`: a web framework, `manage.py`, or a `[project]` without a build backend. Bundle `application`.
- `extension`: maturin, scikit-build-core, meson-python, Cython, pybind11, nanobind, PyO3 or `ext_modules`. Bundles `native-extension`, `library`.
- `cli`: `[project.scripts]` with Typer, Click or Textual. Bundles `cli-and-distribution`, `library`.
- `data-pipeline`: Airflow, Dagster, Prefect, dbt, Spark, DuckDB. Bundle `data-engineering`.
- `ml`: PyTorch, TensorFlow, scikit-learn, JAX, XGBoost, Transformers. Bundle `machine-learning`.
- `llm-app`: Anthropic, OpenAI, LangChain, LiteLLM. Bundle `ai-applications`.
- `mcp-server`: `mcp` or FastMCP. Bundle `agent-tooling`.
- `scraper`: Playwright, Scrapy, Beautiful Soup, Selenium. Bundle `automation-and-scraping`.
- `notebook`: notebooks or Jupyter without a build backend. Bundle `data-analysis`.
- `script`: loose `.py` files or a PEP 723 header. `core` only.
