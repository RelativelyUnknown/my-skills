# databricks-development

Part of the [skills monorepo](../README.md). Run the development commands from this folder.

Six agent skills for data engineering in PySpark and on Databricks. They hold engineering principles: pure transformations, idempotent loads, deliberate table design, tests that run in seconds, tuning from evidence. They are written to sit next to Databricks' official agent skills, not to replace them.

## How this fits with the official Databricks skills

Databricks publishes about 35 product skills in [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills), installed with `databricks aitools install` (they replaced the skills in `databricks-solutions/ai-dev-kit`, which is now deprecated). Those skills document products: bundle YAML, pipeline decorators, jobs, Unity Catalog, streaming options, serverless migration. None of them covers how to structure PySpark code, make loads idempotent, design tables, or test transformations; that is what this skillset is for.

- Install both. When an official skill is present, these skills defer to it for API and YAML details and keep their own rules for structure and correctness.
- The official skills are under the Databricks License (use only with Databricks services), so nothing here is copied from them. Facts were checked against the Databricks and Apache Spark docs.
- Other sources: the [Palantir PySpark style guide](https://github.com/palantir/pyspark-style-guide) (MIT) for code style, [databrickslabs/pylint-plugin](https://github.com/databrickslabs/pylint-plugin) checks (pass `spark` in, no `%run` chains, no `show()` in jobs), and the rule set of [burnt](https://github.com/RelativelyUnknown/burnt), whose codes appear in the anti-pattern table.

## Skills

| Skill | Loads when you... | Body (est. tokens) |
| --- | --- | --- |
| `writing-pyspark-transformations` | write, refactor or review PySpark or Spark SQL transformation logic | 1.8k |
| `building-data-pipelines` | design or change a pipeline, a table load, a MERGE or a stream | 1.8k |
| `designing-delta-tables` | create or alter a table, choose clustering keys, change retention or maintenance | 1.6k |
| `testing-pyspark-code` | add or fix tests for Spark code, or set up the test environment | 1.6k |
| `tuning-spark-jobs` | chase a slow, out-of-memory or expensive job | 1.2k |
| `setting-up-databricks-projects` | create a Databricks repo, edit `databricks.yml` or resources, wire CI/CD | 1.5k |

Always-on cost is the six descriptions: about 470 tokens. Reference files load only when a skill points at them: `anti-patterns.md` and `python-data-sources.md` (transformations), `declarative-pipelines.md`, `merge-and-cdc.md` and `streaming.md` (pipelines).

The skills extend the [python-package-development](../python-package-development/) skills by name (`writing-python-code`, `testing-python-packages`, `setting-up-python-packages`). Install those too, or the cross-references point nowhere.

## Install

```bash
mkdir -p .claude/skills
cp -r /path/to/skills/databricks-development/skills/* .claude/skills/
cp -r /path/to/skills/python-package-development/skills/{writing-python-code,testing-python-packages,setting-up-python-packages} .claude/skills/
databricks aitools install --scope project   # optional: the official product skills
```

**Minimal profile** for PySpark work outside Databricks: `writing-pyspark-transformations` and `testing-pyspark-code`.

## Project detection and arguments

Every skill starts by running `scripts/detect_project.py` (Python 3.11+, standard library only). It prints:

- the bundle, its targets and the default target;
- compute kind (`serverless`, `classic`, `mixed`), runtime and serverless environment versions;
- the Spark client: `pyspark`, `databricks-connect`, or `conflict` when both are declared;
- Spark packages wrongly listed as runtime dependencies;
- notebook and pipeline file counts, and whether pipelines still use `import dlt`;
- missing tools (`databricks`, `java`, `uv`).

It scans YAML line by line rather than parsing it, so unusual layouts print `# default`.

| Key | Values | Default |
| --- | --- | --- |
| `runtime` | Databricks Runtime major version, for example `18` | detected `spark_version`, else current LTS |
| `compute` | `serverless`, `classic` | detected, else `serverless` |
| `target` | bundle target name | the target with `default: true` |

## Facts checked for this version (November 2026)

- Databricks Asset Bundles are now **Declarative Automation Bundles**; the `databricks bundle` commands and YAML are unchanged.
- Delta Live Tables is now **Lakeflow Spark Declarative Pipelines**; Python code uses `from pyspark import pipelines as dp`, and `AUTO CDC` replaces `APPLY CHANGES`.
- Databricks Runtime 18 LTS (Spark 4.1) is the current LTS; Runtime 19 runs Spark 4.2. ANSI mode is on by default.
- Liquid clustering is recommended for all new tables (at most four keys); `CLUSTER BY AUTO` needs DBR 15.4 LTS+ and predictive optimization, which is on by default for Unity Catalog managed tables.
- Serverless supports Spark Connect APIs only, rejects most Spark configs, and supports only `availableNow` streaming triggers.
- `databricks-connect` and `pyspark` cannot share an environment. Serverless environment 5 pairs with `databricks-connect` 18.0 and Python 3.12.

Re-check these when Databricks ships a new LTS; the skills name minimum runtimes where it matters.

## Evals

Each skill has eval cases in `skills/<skill>/evals/` (the `claude plugin eval` layout) and trigger checks in `evals/<skill>.triggers.json`. The cases target what a model gets wrong without the skill: a rerunnable load, a `dlt` migration, clustering instead of partitioning, the `pyspark`/`databricks-connect` split, tuning on serverless.

## Develop

```bash
uv sync
uv run pytest                          # tests for detect_project.py
uv run ruff check scripts tests && uv run mypy scripts tests
cd ../python-package-development && uv run python scripts/check_skills.py \
  --canonical ../databricks-development/scripts/detect_project.py \
  --argument-keys runtime,compute,target ../databricks-development/skills
```

After changing `scripts/detect_project.py`, add `--sync` to the check command to copy it into each skill.

## License

MIT.
