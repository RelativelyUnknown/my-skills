# Structured Streaming and Auto Loader

## Contents

- Auto Loader ingestion
- Triggers
- Checkpoints
- State and watermarks
- Joins
- Operating a stream

## Auto Loader ingestion

```python
bronze = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", schema_location)        # where inferred schema versions live
    .option("cloudFiles.schemaHints", "order_id BIGINT, amount DECIMAL(18,2)")
    .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
    .option("cloudFiles.useManagedFileEvents", "true")           # needs an external location with file events
    .load(source_path)
    .select("*", "_metadata.file_path", "_metadata.file_modification_time",
            F.current_timestamp().alias("ingested_at"))
)
(bronze.writeStream
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(f"{catalog}.{schema}.orders_bronze"))
```

- Known, fixed schema: pass `.schema(...)` and skip inference. Unknown shape: ingest as `VARIANT` (`singleVariantColumn`) and parse downstream.
- `schemaEvolutionMode`: `addNewColumns` (stream stops once, restart picks up the new column), `addNewColumnsWithTypeWidening`, `failOnNewColumns` (strict contract), `rescue` (keep the schema, put new fields in `_rescued_data`). Choose it; do not leave it to the default by accident.
- Keep `_rescued_data` and alert when it is not null. Capture unparsable rows with `columnNameOfCorruptRecord`.
- `cloudFiles.cleanSource` (`move`/`delete`) only when nothing else reads the source directory.
- Write to a table name with `toTable`, not a storage path.

## Triggers

| Trigger | Use |
| --- | --- |
| `availableNow=True` | Process everything new, then stop. Default for scheduled or file-arrival jobs; works on serverless |
| `processingTime="1 minute"` | Always-on micro-batches on classic compute when minutes of latency matter |
| Real-time mode / continuous | Sub-second latency needs only; check the runtime's supported operations first |
| No trigger | Never in production: runs back-to-back micro-batches and fails on serverless |

`Trigger.Once` is deprecated; use `availableNow`.

## Checkpoints

- One checkpoint per query, in a Unity Catalog volume next to the output, never inside the source directory and never under a lifecycle-deletion policy.
- The checkpoint ties the query to its sources and stateful operators. Adding or removing a stateful operator, changing a source, or changing aggregation keys can be incompatible; plan a new checkpoint and a backfill instead of editing in place.
- Name checkpoint paths after the target table and a version (`.../checkpoints/orders_silver/v2`) so a planned reset is explicit.

## State and watermarks

- Every stateful operation (`groupBy` with a time window, `dropDuplicatesWithinWatermark`, stream-stream joins) has `withWatermark(event_time_col, delay)`. The delay is how late data may arrive; later rows are dropped, so pick it from the source's real lateness.
- Deduplicate streams with `dropDuplicatesWithinWatermark(["event_id"])`, not `dropDuplicates` without a watermark (unbounded state).
- Large state on classic compute: enable the RocksDB state store provider. Custom state machines: `transformWithState` (Spark 4 / recent DBR) over the older `applyInPandasWithState`.

## Joins

- Stream-static join: the static side is re-read each micro-batch (Delta) and gives point-in-time-of-processing results, not event-time results. Use a left join from the stream when a missing dimension row must not drop the event.
- Stream-stream join: watermarks on both sides and a time-range condition in the join, or state grows without bound.
- Broadcast hints on a streaming DataFrame fail; do not add them.

## Operating a stream

- Log `query.lastProgress` metrics (input rows, processing rate, batch duration) or use the job's streaming observability; alert on growing backlog.
- A failing micro-batch retries the same offsets: the sink must be idempotent (Delta sink, MERGE with conditions, or `txnAppId`/`txnVersion` in `foreachBatch`).
- Restarting after a code change: check that the change is compatible with the checkpoint before restarting a production stream.
