# Lakeflow Spark Declarative Pipelines

Formerly Delta Live Tables (DLT); also called SDP or LDP. The Python module is `from pyspark import pipelines as dp`; legacy `import dlt` code still runs, with the same decorator names under `dlt.`. For full option lists, use the official `databricks-pipelines` skill when installed, or the Databricks docs.

## Contents

- Migrating from `dlt`
- Dataset types
- Rules for pipeline code
- Flows, sinks and CDC
- Expectations
- Configuration and deployment

## Migrating from `dlt`

Migrate a file only when asked or when you are already changing it; keep each pipeline on one style.

| Legacy | Current |
| --- | --- |
| `import dlt` | `from pyspark import pipelines as dp` |
| `@dlt.table` returning a streaming DataFrame | `@dp.table` |
| `@dlt.table` returning a batch DataFrame | `@dp.materialized_view` |
| `@dlt.view` | `@dp.temporary_view` |
| `dlt.read("x")`, `dlt.read_stream("x")` | `spark.read.table("x")`, `spark.readStream.table("x")` |
| `dlt.create_streaming_table(...)` | `dp.create_streaming_table(...)` |
| `dlt.apply_changes(...)` | `dp.create_auto_cdc_flow(...)` (same arguments) |
| `dlt.apply_changes_from_snapshot(...)` | `dp.create_auto_cdc_from_snapshot_flow(...)` |
| `@dlt.append_flow`, `dlt.create_sink`, `@dlt.expect*` | `@dp.append_flow`, `dp.create_sink`, `@dp.expect*` |
| SQL `APPLY CHANGES INTO` | `AUTO CDC INTO` |
| SQL `CREATE LIVE TABLE` | `CREATE MATERIALIZED VIEW` or `CREATE STREAMING TABLE` |

## Dataset types

| You need | Python | SQL |
| --- | --- | --- |
| Incremental, append-style table from a stream | `@dp.table` returning a streaming DataFrame | `CREATE OR REFRESH STREAMING TABLE ... AS SELECT ... FROM STREAM ...` |
| Table recomputed from batch reads (aggregates, joins over full data) | `@dp.materialized_view` | `CREATE OR REFRESH MATERIALIZED VIEW` |
| Intermediate logic, not published | `@dp.temporary_view` | `CREATE TEMPORARY VIEW` |
| Empty target that flows write into | `dp.create_streaming_table(name, ...)` | `CREATE OR REFRESH STREAMING TABLE name` |

- A streaming table processes each input row once; it does not recompute when an upstream row changes. Aggregations over a stream that must stay correct belong in a materialized view with a batch read.
- Changing a dataset between streaming table and materialized view is not an in-place change; define a new name and repoint consumers.
- Read sources with `spark.read.table(...)` / `spark.readStream.table(...)`; `dp.read` and `dp.read_stream` are legacy.

## Rules for pipeline code

- A dataset function returns a DataFrame and does nothing else. No `collect()`, `count()`, `toPandas()`, `save`/`saveAsTable`, `writeStream.start()` or `spark.conf.set` inside it. The pipeline evaluates these functions while planning, possibly more than once.
- Helper logic lives in importable modules shared with tests; the pipeline file wires datasets together. Declare Python dependencies in the pipeline's environment, not with `%pip` in a source file.
- Parameterize catalog, schema and paths through pipeline configuration (`spark.conf.get("my.param")`) set by the bundle, not literals.
- One pipeline owns each table. Do not write to a pipeline-owned table from a job or another pipeline.

## Flows, sinks and CDC

- Several sources into one table: `dp.create_streaming_table(target)` plus one `@dp.append_flow(target=target)` per source. Not a `union` of streams, which couples their checkpoints.
- Historical backfill plus live feed: an `append_flow` with `once=True` for the backfill and a regular flow for the stream.
- Writing to a table the pipeline does not own, Kafka or Event Hubs: `dp.create_sink(...)` with an `append_flow` to it. Custom per-batch logic (for example a MERGE into an external table): a for-each-batch sink. Sinks are Python only.
- CDC into a pipeline-owned table: `dp.create_streaming_table(target)` then `dp.create_auto_cdc_flow(target=..., source=..., keys=[...], sequence_by=..., stored_as_scd_type=1 or "2", apply_as_deletes=..., except_column_list=[...])`. SQL: `AUTO CDC INTO target FROM stream(source) KEYS (...) SEQUENCE BY ... STORED AS SCD TYPE 2`. `AUTO CDC` replaces the older `APPLY CHANGES` with the same arguments.
- Snapshots instead of a change feed: `dp.create_auto_cdc_from_snapshot_flow(...)`.
- The sequence column must be sortable and never null. Ties on one column: sequence by a struct (`F.struct("ts", "id")`).
- SCD type 2 targets carry `__START_AT` and `__END_AT`; current rows have `__END_AT IS NULL`. Consumers that need changes from an `AUTO CDC` target read its change data feed.
- `AUTO CDC` needs serverless pipelines or the Pro/Advanced edition and is Databricks only, not in open-source Spark Declarative Pipelines.

## Expectations

| Decorator | On violation |
| --- | --- |
| `@dp.expect(name, sql_condition)` | Keep the row, record the metric |
| `@dp.expect_or_drop(name, sql_condition)` | Drop the row, record the metric |
| `@dp.expect_or_fail(name, sql_condition)` | Fail the update |
| `@dp.expect_all`, `expect_all_or_drop`, `expect_all_or_fail` | Same, with a `{name: condition}` dict |

- Name each expectation for the rule it enforces (`valid_order_id`), so the event log reads as a report.
- Keys and other fields the output's correctness depends on use `expect_or_fail`. Use `expect_or_drop` only when dropping is the documented rule, and quarantine rows you might need: a second dataset with the inverted condition.
- Check `_rescued_data IS NULL` on bronze tables fed by Auto Loader to surface schema drift.

## Configuration and deployment

- Define pipelines in the bundle (`resources/<name>.pipeline.yml`) with `catalog`, `schema`, `serverless: true` and a `libraries` glob over the transformations folder.
- Development mode (bundle `mode: development`) reuses compute and does not retry on failure; production retries. Run a validation (dry run) update after changes before a full refresh.
- Full refresh truncates streaming tables and reprocesses all source data. It needs approval, and sources whose retention has passed cannot be replayed.
