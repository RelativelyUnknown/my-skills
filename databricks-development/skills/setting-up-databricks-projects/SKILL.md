---
name: setting-up-databricks-projects
description: "Scaffolds or audits a Databricks code project: Declarative Automation Bundles (formerly Asset Bundles), src-layout wheel, thin notebooks, dev/prod targets, runtime-matched local environment, secrets, CI/CD with GitHub OIDC. Use when creating a Databricks repo or editing databricks.yml, job or pipeline resources, or deployment workflows."
argument-hint: "[runtime=18 compute=serverless target=dev]"
---

# Setting up Databricks projects

Treat a Databricks project as a Python package that a bundle deploys. Logic is importable and tested; notebooks, jobs and pipelines are thin wiring. Python packaging rules (`pyproject.toml`, uv, ruff, typing) come from `setting-up-python-packages`.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`bundle`, `bundle.targets`, `compute`, `runtime`, `serverless.environment_version`, `spark.client`, `spark.in_runtime_deps`, `notebooks`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts.

- **Existing project: keep its structure and tools.** Do the task within them and list differences from the defaults below as suggestions.
- If the official Databricks skills are installed (`databricks aitools install`; for example `databricks-dabs`, `databricks-core`), use them for exact resource schemas and CLI flags. This skill decides structure and rules.
- Never `databricks bundle deploy` or `run` to a target other than `dev` unless asked; never deploy production from a laptop. Never write a token, host secret or personal email into the repository.

## Layout

```
project/
├── databricks.yml              # bundle name, variables, targets
├── resources/                  # one file per resource: <name>.job.yml, <name>.pipeline.yml
├── src/<pkg>/
│   ├── transforms/             # DataFrame -> DataFrame functions; no I/O
│   ├── pipelines/              # declarative pipeline definitions (dp.table, flows)
│   └── jobs/                   # entry points: parse args, get spark, read, transform, write
├── notebooks/                  # optional: exploration or thin entry points only
├── tests/unit/  tests/integration/
└── pyproject.toml  uv.lock
```

- Business logic lives in `src/<pkg>` and is imported. Notebooks call package functions; `%run` chains and copy-pasted cells are replaced by imports.
- Job tasks run the wheel: `python_wheel_task` with an entry point from `[project.scripts]`, or a pipeline task. Entry points take parameters as arguments (`--catalog`, `--schema`, `--run-date`); `dbutils.widgets` appears only in notebooks.
- Catalog and schema are bundle variables set per target and passed to code. Library code always uses three-part names built from those parameters; it never relies on `USE CATALOG` or a hard-coded catalog.
- Start from [assets/databricks.yml](assets/databricks.yml) and [assets/job.yml](assets/job.yml).

## Targets

- `dev`: `mode: development` (resources prefixed with the developer's name, schedules paused), `default: true`, schema per developer (`${workspace.current_user.short_name}`).
- `prod` (and `staging` if used): `mode: production`, a fixed `root_path`, `run_as` a service principal, permissions granted to groups. Production deploys only from CI.
- After any change to bundle files: `databricks bundle validate --strict -t <target>`. Review `databricks bundle plan -t <target>` before deploying to a shared target.
- New bundles deploy with the direct deployment engine (default since CLI 1.3); existing Terraform-engine bundles keep working. Do not switch an existing bundle's engine unasked.

## Compute and dependencies

- Default to serverless jobs and pipelines: an `environments` entry with `environment_version` and the wheel as a dependency. Use classic job clusters (`spark_version` on an LTS runtime) only for what serverless lacks: RDD or Scala code, init scripts, custom Spark configs, specific instance types. Never run jobs on all-purpose clusters.
- Pin the runtime: an LTS `spark_version` for classic, an explicit `environment_version` for serverless. Upgrades are deliberate changes with a test run.
- `[project].dependencies` lists only what the code imports that the runtime lacks. Never `pyspark`, `databricks-connect` or `delta-spark` there (`spark.in_runtime_deps` flags this); the runtime provides them.
- Match local Python and libraries to the target compute: Databricks Runtime 16.4 and up and serverless environments 3 and up use Python 3.12. `databricks environments setup-local` (CLI 1.16+) builds a matching uv environment; the `databricks/environments` repository publishes the pins it uses.
- Local `pyspark` (unit tests) and `databricks-connect` (remote runs) go in separate, conflicting dependency groups; see `testing-pyspark-code`.

## Secrets and identity

- Secrets come from secret scopes (`dbutils.secrets.get(scope, key)`) or Unity Catalog connections and service credentials, read at runtime. Never in code, YAML, job parameters or notebook output.
- Humans authenticate with OAuth (`databricks auth login`), not personal access tokens. CI uses a service principal through GitHub OIDC workload identity federation (`DATABRICKS_AUTH_TYPE=github-oidc`); no long-lived token is stored.

## CI/CD

Copy [assets/deploy.yml](assets/deploy.yml). It runs lint and unit tests on every pull request (no workspace access needed), then validates and deploys the bundle to `prod` from `main` through a protected GitHub environment. Add the type checker to the check job if the project uses one.

- A person must create the service principal, its federation policy (subject `repo:<org>/<repo>:environment:prod` or the ID-based form for newer repositories) and the GitHub environment; say so, do not try to do it.
- Pin `databricks/setup-cli` and other actions to a release tag. Grant `id-token: write` only to the deploy job.
- Integration tests and end-to-end runs deploy to `dev` or `staging` with the same bundle, never a hand-built copy.

## New project checklist

1. `pyproject.toml` (uv, hatchling or uv_build, ruff, type checker, pytest) per `setting-up-python-packages`; `requires-python` matching the target compute.
2. `databricks.yml` with `catalog`/`schema` variables and `dev`/`prod` targets; one resource file per job or pipeline.
3. Unit tests run locally without a workspace; one command runs lint, types and unit tests.
4. `databricks bundle validate --strict` passes for every target.
5. `.gitignore` covers `.databricks/`, `.venv/`, `dist/`, `__pycache__/`, `*.egg-info/`.

Run the check command and `bundle validate` and show the output. A scaffold you did not run is not done.
