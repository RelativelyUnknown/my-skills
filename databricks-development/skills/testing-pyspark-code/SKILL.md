---
name: testing-pyspark-code
description: "Tests PySpark and Databricks code: local SparkSession fixtures, assertDataFrameEqual, small explicit inputs, Databricks Connect integration tests, idempotency and MERGE tests, separating pyspark from databricks-connect. Use when adding or fixing tests for Spark transformations, pipelines or jobs, or setting up their test environment."
argument-hint: "[runtime=18 compute=serverless]"
---

# Testing PySpark code

Most Spark bugs are logic bugs visible on ten rows: a join that multiplies, a null that slips through, a window frame that is off by one. Test the logic locally in seconds; test the platform wiring separately. The general test rules (never weaken a test, a bug fix starts red, expected values come from the spec) are in `testing-python-packages` and apply here unchanged.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`spark.client`, `runtime`, `compute`, `test.tools`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts.

- `spark.client=conflict`: `pyspark` and `databricks-connect` are declared in one environment. They cannot be installed together; split them as below before anything else.
- `tools.missing` contains `java`: local Spark cannot start. PySpark 4.x needs Java 17 or 21. Report it; do not install a JDK silently.
- Use the plugins and assertion helpers already in `test.tools` (for example `chispa`); add none unprompted.

## Three levels

| Level | Runs on | Tests | Speed |
| --- | --- | --- | --- |
| Unit | Local `SparkSession` (`pyspark` pinned to the runtime's Spark version) | Pure transformation functions on tiny DataFrames | Seconds; every commit |
| Integration | Databricks Connect against a dev workspace, or local Spark with `delta-spark` | Reads and writes of real tables, MERGE logic, Unity Catalog names | Minutes; before merge |
| End to end | The deployed bundle on the `dev` target | Job or pipeline runs; assert on output tables | Slowest; on main or nightly |

Put most tests at the unit level. That only works when logic is in functions that take and return DataFrames (`writing-pyspark-transformations`); if it is buried in a notebook, extracting it is part of the task.

## Environments

`databricks-connect` replaces `pyspark` with its own client, so the two live in separate dependency groups that uv will not install together:

```toml
[dependency-groups]
dev = ["pytest>=8"]
spark-local = ["pyspark==4.1.*"]                 # match the cluster's Spark version
spark-remote = ["databricks-connect~=18.0.0"]    # match the runtime or serverless environment

[tool.uv]
conflicts = [[{ group = "spark-local" }, { group = "spark-remote" }]]
```

Run units with `uv run --group spark-local pytest tests/unit` and integration with `uv run --group spark-remote pytest tests/integration`. Pin `databricks-connect` to the target runtime's version (`~=18.0.0` for DBR 18.0 and serverless environment 5); a client newer than the runtime is not supported. Neither belongs in `[project].dependencies`; the runtime provides Spark.

## The local session

```python
# tests/unit/conftest.py
import pytest
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("unit-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.ansi.enabled", "true")   # match Databricks and Spark 4 behaviour
        .getOrCreate()
    )
    yield session
    session.stop()
```

- Session scope: starting Spark costs seconds; tests share one session and never change its config.
- PySpark talks to its JVM over a localhost socket. With `pytest-socket`, use `--allow-hosts=127.0.0.1,localhost` instead of `--disable-socket`.
- Code that must also run on serverless: occasionally run the unit suite through Spark Connect (`spark.api.mode=connect` on Spark 4) to catch RDD and `sparkContext` use.

## Writing the tests

- Build inputs inline with an explicit schema: `spark.createDataFrame(rows, "id BIGINT, amount DECIMAL(10,2), ts TIMESTAMP")`. A handful of rows per test, each one there for a reason. No CSV fixtures for logic tests; no sampled production data.
- Compare whole DataFrames: `from pyspark.testing import assertDataFrameEqual, assertSchemaEqual`. `assertDataFrameEqual(actual, expected)` ignores row order by default and takes `rtol`/`atol` for floats. Check the output schema with `assertSchemaEqual` when the schema is part of the contract.
- Never assert only `df.count() > 0` or `is not None`. Assert the exact expected rows, written by hand from the spec.
- Cover, for each transformation: nulls in keys and values, duplicate keys, an empty input, boundary dates and time zones, late or out-of-order records, and values that ANSI mode rejects.
- Joins: one test where a key has no match and one where it has several, with the expected row count written out.
- One behavior per test, named for it: `test_late_update_does_not_overwrite_newer_row`.

## Pipeline properties worth a test

- **Idempotency**: run the load twice on the same input into a temp table; assert the table equals one run's result.
- **Order independence**: apply the same changes in two batch orders; assert the same final state when the sequence column says it should be.
- **Key uniqueness**: `df.groupBy(*keys).count().filter("count > 1").isEmpty()` on the output.
- **MERGE and Delta behaviour**: needs Delta. Locally use `delta-spark` matched to the Spark version (`configure_spark_with_delta_pip`) in a separate session fixture over `tmp_path`, or test it at the integration level.
- **Streams**: write test files into `tmp_path`, run the query with `trigger(availableNow=True)` and a checkpoint in `tmp_path`, wait with `awaitTermination()`, then assert on the sink. Run it twice to prove the checkpoint prevents reprocessing.

## Integration tests on Databricks

- Use a dedicated dev catalog or a schema created per test run and dropped afterwards; never production names. `databrickslabs/pytester` fixtures (`make_schema`, `make_table`) create and clean up workspace objects.
- Mark them (`@pytest.mark.integration`) and keep them out of the default run; they need credentials from the environment, never from the repository.
- Serverless or cluster is chosen by the Databricks Connect configuration (profile, `DATABRICKS_SERVERLESS_COMPUTE_ID=auto`, or cluster ID), not in test code.

## Report

List tests added, changed or removed with reasons, the level of each, the commands run with results, and any behavior left untested because it needs a workspace.
