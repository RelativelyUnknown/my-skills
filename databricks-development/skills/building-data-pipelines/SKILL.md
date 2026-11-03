---
name: building-data-pipelines
description: "Data engineering rules for Spark and Databricks pipelines: idempotent writes, incremental ingestion, MERGE and CDC, medallion layer contracts, streaming checkpoints, data quality, backfills, declarative pipelines vs jobs. Use when designing or changing a pipeline, a table load, a MERGE or a stream."
argument-hint: "[runtime=18 compute=serverless target=dev]"
---

# Building data pipelines

A pipeline is correct when running it twice, late or after a crash leaves the same tables as running it once on time. Design for that first; speed second. Transformation code follows `writing-pyspark-transformations`.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`compute`, `runtime`, `pipelines.api`, `bundle.targets`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts.

- `pipelines.api=dlt` means legacy `import dlt` code. Write new code with `from pyspark import pipelines as dp`; migrate existing files only if asked.
- Never run a pipeline, `bundle deploy` or a write against a non-dev target unless asked. Dropping or overwriting a table, `VACUUM` with short retention, `RESTORE`, full refreshes and checkpoint deletion need approval: each can lose data or reprocess everything.

## Before writing code, write down

1. **Grain and key** of the target: one row per what, unique on which columns.
2. **Source behaviour**: append-only files, CDC feed with operation and sequence columns, periodic full snapshots, or a mutable table. This decides the write pattern.
3. **Freshness and volume**: how late, how often, how much. Batch every hour on a schedule is a fine answer.
4. **What happens to bad rows**: fail the run, drop and count, or quarantine.

## Idempotent writes

Pick the pattern from the source behaviour. Every write must survive a retry.

| Source | Write | Idempotent because |
| --- | --- | --- |
| Append-only files or events | Auto Loader / streaming read with `trigger(availableNow=True)` into an append target | Checkpoint records what was processed |
| CDC feed (insert/update/delete, sequence column) | `AUTO CDC` in a declarative pipeline, or MERGE from a deduplicated batch | Latest change per key wins by sequence |
| Periodic full snapshot | `AUTO CDC ... FROM SNAPSHOT`, or MERGE with `WHEN NOT MATCHED BY SOURCE` | Target is diffed against the snapshot |
| Recompute a bounded slice (a day, a region) | `replaceWhere` overwrite of exactly that slice | Same slice in, same slice out |
| Small dimension rebuilt each run | `CREATE OR REPLACE TABLE` / full overwrite | Whole table is the unit |

- Never `mode("overwrite")` a whole table for a partial load. Never blind-append a batch that a retry can append again.
- `foreachBatch` writes are idempotent only through MERGE or the Delta writer options `txnAppId` and `txnVersion` (use the batch ID).
- Each streaming query has its own checkpoint in a Unity Catalog volume; never share, move or delete one without approval. Changing the query's logic may require a new checkpoint; say so.

## MERGE

- Deduplicate the source to one row per key first (latest by the sequence column). Otherwise MERGE fails with `DELTA_MULTIPLE_SOURCE_ROW_MATCHING_TARGET_ROW_IN_MERGE`, or worse, applies an arbitrary row.
- Put clustering or partition columns in the `ON` condition when the source covers a known range, so the merge prunes files.
- `WHEN MATCHED AND <something changed> THEN UPDATE`: updating unchanged rows rewrites files for nothing. Compare a row hash or the sequence column.
- Deletes from a snapshot use `WHEN NOT MATCHED BY SOURCE [AND <scope>] THEN DELETE`; always scope it when the source covers only part of the target.
- Schema changes in a MERGE are explicit: `MERGE WITH SCHEMA EVOLUTION` (DBR 15.2+) on that statement, never session-wide auto-merge.

## Layers

Medallion layers are contracts, not folders:

- **Bronze**: source data as received, append-only, plus ingestion metadata (`_metadata.file_path`, `_metadata.file_modification_time`, ingest time). Keep `_rescued_data`. No business logic, so it can be replayed.
- **Silver**: typed, deduplicated, conformed; one documented grain and key per table; data-quality rules applied.
- **Gold**: shaped for consumers (aggregates, dimensional models, features). Each gold table names its consumer.

Skip a layer when it adds nothing; do not create empty pass-through tables. Each table has a comment stating grain, key and source (`designing-delta-tables`).

## Incremental processing

- Files: Auto Loader (`cloudFiles`) with an explicit schema or `schemaHints`, a schema location, and `schemaEvolutionMode` chosen on purpose (`addNewColumns`, `addNewColumnsWithTypeWidening`, `failOnNewColumns`). Prefer managed file events (`cloudFiles.useManagedFileEvents`) over directory listing.
- Downstream of Delta tables: stream from the table, or read its change data feed (`readChangeFeed` from a stored version) when you need updates and deletes.
- Batch on a schedule or file-arrival trigger with `availableNow` instead of an always-on stream unless the latency need is real. Serverless rejects `processingTime` and continuous triggers.
- Stateful streams (aggregations, dedupe, stream-stream joins) need a watermark; without one, state grows forever.

## Data quality

- Rules live next to the table: expectations in declarative pipelines (`@dp.expect`, `expect_or_drop`, `expect_or_fail`), `CHECK` and `NOT NULL` constraints on Delta tables, or a checks library such as DQX in plain jobs.
- Fail on violations that make the output wrong (null keys, duplicate keys, broken referential integrity). Drop or quarantine rows only when the rule says so, and record the count.
- Quarantine means a table of rejected rows with the reason and the run ID, not a silent filter.

## Backfills and reruns

- Parameterize every job by the slice it processes (date range, batch ID). A backfill runs the same code with a different range, never a copied notebook.
- Derive "now" once per run and pass it down; do not call `current_date()` in several places.
- Reprocessing a stream from scratch is a deliberate operation (new checkpoint, target rebuilt or deduplicated). Write down the steps before doing it.

## Declarative pipelines or jobs

Use Lakeflow Spark Declarative Pipelines when the work is a graph of tables with streaming ingestion, CDC (`AUTO CDC`), expectations and managed refresh. Use jobs running plain PySpark from a wheel when you need imperative control: writes to tables the pipeline does not own, complex orchestration, external side effects, or full control of the write. Do not mix both owners on one table.

## Read when relevant

| Doing | Read |
| --- | --- |
| Writing or changing a declarative pipeline (`dp.table`, flows, sinks, `AUTO CDC`) | [references/declarative-pipelines.md](references/declarative-pipelines.md) |
| Writing a MERGE, SCD type 1/2 or CDC logic by hand | [references/merge-and-cdc.md](references/merge-and-cdc.md) |
| Writing a Structured Streaming query or Auto Loader ingestion | [references/streaming.md](references/streaming.md) |

Table design and maintenance: `designing-delta-tables`. Project layout and deployment: `setting-up-databricks-projects`.

## Report

State the write pattern chosen and why it is idempotent, every table and checkpoint created or changed, any operation that needs approval and whether you ran it, and how a rerun or backfill behaves.
