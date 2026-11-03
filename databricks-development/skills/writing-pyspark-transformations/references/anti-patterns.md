# PySpark anti-patterns

Each row: the pattern, why it hurts, and the fix. Codes in brackets are the matching `burnt check` rules, for projects that run burnt. A pattern is a finding only when the fix applies; say why when it does not.

## Contents

- Driver and actions
- Plans and columns
- Joins and windows
- Reading and writing
- Correctness and determinism
- Configuration

## Driver and actions

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| `collect()` or `toPandas()` on unbounded data [BP008, BP011] | Pulls every row into driver memory; out-of-memory or a slow single-threaded step | Aggregate or `limit(n)` first; write results to a table |
| `.rdd`, `rdd.map`, `toJSON().collect()` [BNT-A04, BP101, BP112] | Leaves the optimized engine; rows become Python objects; unavailable on serverless | DataFrame functions, `mapInPandas`/`mapInArrow` if row-wise Python is unavoidable |
| `count()` to test emptiness [BP016] | Scans the whole input | `df.isEmpty()` |
| `show()`, `display()`, `explain()`, `print(df.count())` in pipeline code [BO001-BO003] | Each one runs a job; output is discarded in jobs | Remove; log metrics from `df.observe` or write metrics |
| Same DataFrame hit by two actions without caching [BP032] | Plan executes twice | Combine into one action, or `cache()` then `unpersist()` |
| `cache()` on a DataFrame used once, or never unpersisted [BP030, BP031] | Memory pressure with no reuse | Remove, or `unpersist()` after the last use |

## Plans and columns

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| `withColumn` in a loop [BP020] | Plan grows per call; analysis time grows quadratically | `withColumns({...})` or one `select` |
| Long chains of `withColumn` [BP074] | One projection per call | `withColumns({...})` |
| Python UDF for logic a built-in covers [BP010, BP100] | Row-by-row serialization to Python; no Photon | Built-in function, SQL expression, higher-order function |
| pandas UDF where a built-in exists [BP015] | Still serializes through Arrow | Built-in; keep pandas UDFs for logic Spark cannot express |
| `from pyspark.sql.functions import *` [BNT-I01] | Shadows Python built-ins `sum`, `max`, `round`, `filter` | `from pyspark.sql import functions as F` |
| `toDF(*names)` to rename [BNT-A01] | Renames by position; silently wrong when columns move | `withColumnsRenamed({...})` or `select` with aliases |
| `df.col` / `df["col"]` everywhere [BNT-C01] | Binds to a specific DataFrame; stale after reassignment | `F.col("col")`; qualified names via aliases after joins |
| `orderBy` before a shuffle [BP073] | The shuffle discards the order | Sort last, or not at all |
| `repartition(1)` or `coalesce(1)` to get one file [BP012] | One task does all the work | Let Delta manage file sizes; one file is rarely a requirement |

## Joins and windows

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| Join without `how=`, or a right join | Hides intent; invites picking the wrong side | Explicit `how=`; left join with the driving table on the left |
| Join to a non-unique key, then `dropDuplicates()` | Row explosion hidden by an arbitrary dedupe | Make the key unique upstream; assert uniqueness |
| Join on columns of different types [BJ001] | Implicit cast changes values or blocks optimizations | Cast explicitly before the join |
| Self-join without aliases [BJ002] | Ambiguous column references | `df.alias("a")`, `df.alias("b")`, qualified selects |
| `crossJoin` or a join with no condition [BP014] | Output is rows(a) x rows(b) | A real join condition; cross join only for tiny, intended cases |
| `Window.partitionBy()` empty, or `orderBy` without `partitionBy` [BP023] | All rows go to one task | Aggregate, or partition the window |
| Window without an explicit frame where the result depends on it | Default frame changes when `orderBy` is added | `rowsBetween` / `rangeBetween` |
| `broadcast()` hint on a table that grows | Driver and executor memory blow-up later | Let AQE decide; hint only with a measured reason |

## Reading and writing

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| `inferSchema=True` on CSV or JSON [BP050, BP053] | Reads the data twice; types drift between runs | Explicit schema; Auto Loader with `schemaHints` |
| Streaming read of JSON/CSV without a schema [BP052] | Inference at every restart | Explicit schema or Auto Loader schema location |
| `mode("overwrite")` on a whole table for a partial load [BD010] | Replaces data the run did not produce | `replaceWhere` on the slice, or MERGE |
| `.write` inside a loop [BD016] | One small job and small files per iteration | Union the pieces and write once |
| Writing analytical tables as CSV, JSON or Parquet [BD013, BD014] | No ACID, no schema enforcement, no time travel | Delta (or managed Iceberg) tables in Unity Catalog |
| `saveAsTable` without `.format("delta")` on older clusters [BD015] | May create a non-Delta table | Explicit format, or `writeTo(name).using("delta")` |
| JDBC read without `partitionColumn`, bounds and `numPartitions` [BP021] | Single-threaded read of the whole table | Partitioned JDBC read, or Lakeflow Connect / federation |
| `writeStream` without `checkpointLocation` [BS001] | Restart reprocesses from the beginning | Unique checkpoint per stream, in a volume |
| `foreachBatch` writing without idempotency [BS004] | Retries duplicate rows | MERGE, or `txnAppId` + `txnVersion` options |

## Correctness and determinism

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| `monotonically_increasing_id()` as a key [BP090] | Values change on recomputation | Hash of natural key columns |
| `rand()`/`randn()` without seed, `uuid()` [BP092, BP093] | Different result per run and retry | Seed it, or derive from data |
| `input_file_name()` as a key [BP094] | Path varies by run; Databricks deprecates it and some access modes reject it | `_metadata.file_path` for lineage only |
| `current_timestamp()` in a cached DataFrame [BP091] | Frozen at first evaluation | Pass the run timestamp as a parameter |
| `dropDuplicates()` without a subset [BP071] | Compares every column; keeps an arbitrary row | `row_number()` over the key ordered by a sequence column |
| `NOT IN` with a nullable subquery [BQ001] | Returns no rows when any value is null | Left anti join, or `NOT EXISTS` |
| `UNION` where duplicates are fine [BQ002] | Extra shuffle to deduplicate | `UNION ALL` / `unionByName` |
| `union` by position | Silently misaligns columns | `unionByName(allowMissingColumns=...)` |

## Configuration

| Pattern | Why it hurts | Fix |
| --- | --- | --- |
| `spark.sql.shuffle.partitions` hard-coded [BP040] | Fights adaptive coalescing | Leave unset; on classic Databricks consider `auto` |
| AQE or its skew/coalesce features disabled [BP041, BP044, BP045] | Loses runtime join and partition optimizations | Keep AQE on |
| `autoBroadcastJoinThreshold = -1` [BP046] | Every dimension join shuffles | Keep the default |
| `spark.databricks.delta.retentionDurationCheck.enabled = false` [BC002] | `VACUUM` can delete files readers still need | Keep the 7-day minimum retention |
| Session-wide `spark.databricks.delta.schema.autoMerge.enabled` [BC003] | Every write may change a schema | `mergeSchema` on the one write that needs it, or explicit `ALTER TABLE` |
| `spark.sql.legacy.*` flags [BC001] | Hide real compatibility bugs | Fix the code for current behaviour |
