# MERGE, CDC and slowly changing dimensions by hand

Use this when a declarative pipeline's `AUTO CDC` does not fit: the target is owned by a job, the logic needs custom conditions, or the code must run on open-source Spark with Delta Lake.

## Contents

- Deduplicate the source
- Upsert (SCD type 1)
- Snapshot sync with deletes
- SCD type 2
- MERGE from a stream
- Checks

## Deduplicate the source

One row per key, the latest by a sequence column that never ties. Without this, MERGE fails or applies an arbitrary change.

```python
from pyspark.sql import Window, functions as F

latest_first = Window.partitionBy("customer_id").orderBy(F.col("sequence_num").desc())
changes = (
    raw_changes
    .withColumn("_rank", F.row_number().over(latest_first))
    .filter(F.col("_rank") == 1)
    .drop("_rank")
)
```

## Upsert (SCD type 1)

```python
from delta.tables import DeltaTable

target = DeltaTable.forName(spark, f"{catalog}.{schema}.customers")
(
    target.alias("t")
    .merge(changes.alias("s"), "t.customer_id = s.customer_id")
    .whenMatchedDelete(condition="s.operation = 'DELETE'")
    .whenMatchedUpdate(
        condition="s.operation != 'DELETE' AND s.sequence_num > t.sequence_num",
        set={"name": "s.name", "email": "s.email", "sequence_num": "s.sequence_num"},
    )
    .whenNotMatchedInsert(
        condition="s.operation != 'DELETE'",
        values={"customer_id": "s.customer_id", "name": "s.name", "email": "s.email",
                "sequence_num": "s.sequence_num"},
    )
    .execute()
)
```

- `s.sequence_num > t.sequence_num` makes the merge safe to replay and ignores out-of-order old changes.
- List columns explicitly. `updateAll()`/`UPDATE SET *` silently picks up new source columns and rewrites unchanged rows.
- Every `whenMatched*` clause except the last needs a condition; the same holds for `whenNotMatched*`.

## Snapshot sync with deletes

When the source is a full snapshot of a scope, delete target rows missing from it, limited to that scope:

```sql
MERGE INTO main.sales.stores AS t
USING snapshot AS s
ON t.store_id = s.store_id
WHEN MATCHED AND t.row_hash <> s.row_hash THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
WHEN NOT MATCHED BY SOURCE AND t.region = 'EU' THEN DELETE
```

`WHEN NOT MATCHED BY SOURCE` needs DBR 12.2 LTS+ or Delta Lake 2.3+. Without the `AND t.region = ...` scope, a partial snapshot deletes everything outside it.

## SCD type 2

Prefer `AUTO CDC ... STORED AS SCD TYPE 2`. By hand, each changed key closes its current row and inserts a new one. The usual single-MERGE form stages each change twice: once with a null merge key (forces an insert of the new version) and once with the real key (closes the current version).

```python
current = spark.read.table(target_name).filter("is_current")
changed = (
    changes.alias("s")
    .join(current.alias("t"), "customer_id", how="inner")
    .filter("s.row_hash <> t.row_hash")
    .select("s.*")
)
staged = (
    changes.withColumn("merge_key", F.col("customer_id"))
    .unionByName(changed.withColumn("merge_key", F.lit(None).cast("bigint")))
)
(
    DeltaTable.forName(spark, target_name).alias("t")
    .merge(staged.alias("s"), "t.customer_id = s.merge_key AND t.is_current")
    .whenMatchedUpdate(
        condition="t.row_hash <> s.row_hash",
        set={"is_current": "false", "valid_to": "s.effective_at"},
    )
    .whenNotMatchedInsert(
        values={"customer_id": "s.customer_id", "name": "s.name", "row_hash": "s.row_hash",
                "is_current": "true", "valid_from": "s.effective_at", "valid_to": "null"},
    )
    .execute()
)
```

Test it with a key that changes twice in one batch, a key that does not change, and a late change older than the current version; decide and document what each should do.

## MERGE from a stream

Run the MERGE inside `foreachBatch`, deduplicating within the batch first. The MERGE is idempotent on replay only when its conditions are (sequence comparison, row hash). Otherwise set `txnAppId` and `txnVersion` on Delta writes inside the batch function.

```python
def upsert_batch(batch, batch_id: int) -> None:
    deduped = latest_per_key(batch)
    merge_into_target(deduped)  # conditions make a replayed batch a no-op

(stream.writeStream
    .foreachBatch(upsert_batch)
    .option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .start())
```

## Checks

- The `ON` condition includes a clustering or partition column whenever the batch covers a bounded range, so the merge reads few files.
- Use `MERGE WITH SCHEMA EVOLUTION` (DBR 15.2+) only when the change is intended; otherwise schema drift fails the merge, which is the safe default.
- After a merge, `DESCRIBE HISTORY <table>` shows `operationMetrics` (rows inserted, updated, deleted). Log them; an update count equal to the whole table usually means a missing change condition.
