---
name: writing-pyspark-transformations
description: "Rules for PySpark DataFrame code: pure DataFrame-in, DataFrame-out functions, schema contracts, joins, windows, nulls, built-ins over UDFs, no driver collects, determinism. Use when writing, refactoring or reviewing PySpark or Spark SQL transformation logic, on Databricks or elsewhere."
argument-hint: "[runtime=18 compute=serverless]"
---

# Writing PySpark transformations

Spark code is a query plan you assemble in Python. Write it so a reader can see the plan, a test can run it on ten rows, and the optimizer can push work down. These rules extend `writing-python-code` (errors, naming, minimalism); they do not repeat it.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root. It prints `runtime`, `compute`, `spark.client`, `pipelines.api`, `python.target` and `tools.missing`; `# default` means nothing was found. Arguments (`key=value` after the skill name) override detected facts.

- `compute=serverless` means Spark Connect only: no RDD API, no `sparkContext`, no `df.checkpoint()`, no `spark.catalog.cacheTable()`, most Spark configs rejected. Write code that runs on both unless the project is classic only.
- Databricks Runtime 17+ and Spark 4 run with ANSI SQL mode on: a bad cast or overflow raises instead of returning null. Use `try_cast` and the `try_*` functions where bad input is expected, and fix the data where it is not.

## Structure

- A transformation is a function that takes DataFrames (and plain parameters) and returns a DataFrame. It does no I/O, triggers no action and reads no global state. Reading and writing happen in a thin entry point at the edge.
- Pass `spark` in when a function needs it; never create a session or refer to a module-level `spark` inside library code. Notebook globals (`spark`, `dbutils`, `display`) exist only in notebooks.
- Chain custom steps with `df.transform(step, arg)`. Keep a chain to about five operations of one kind (select and filter, then derive, then join); past that, extract a named function. Wrap chains in parentheses, never `\`.
- One import style: `from pyspark.sql import functions as F` (or the project's existing alias). Never `from pyspark.sql.functions import *`; it shadows `sum`, `max`, `round` and `filter`.
- Refer to columns with `F.col("name")` or a string. Use `df.col` or `df["col"]` only to disambiguate after a join, through an alias.

## Schema contracts

- Read with an explicit schema (`StructType` or a DDL string). No `inferSchema=True` in pipelines; it scans the data twice and drifts.
- Start and end a transformation with a `select` that names the columns it needs and the columns it returns, with types cast and aliases applied. The output schema is part of the function's contract and its tests.
- Add or rename many columns at once with `withColumns({...})` and `withColumnsRenamed({...})`. Never call `withColumn` in a loop; each call adds a projection to the plan.
- Money and exact quantities are `DecimalType(p, s)`, never float. Timestamps are timezone-aware `TIMESTAMP` in UTC unless the domain needs `TIMESTAMP_NTZ`; parse with an explicit format.
- Semi-structured JSON with a known shape: `from_json` with a schema. Unknown or changing shape on Spark 4 / DBR 15.3+: store as `VARIANT` (`parse_json`) and extract fields where needed.
- Empty typed column: `F.lit(None).cast("string")`, never an untyped `lit(None)`.

## Joins

- Always pass `how=` explicitly. No right joins; swap the DataFrames and use a left join.
- Before joining, know whether the key is unique on the side you expect. A left join to a non-unique key multiplies rows. Assert it in a test or a data-quality check; never cover it with `dropDuplicates()` or `distinct()`.
- Drop or rename overlapping columns before the join, or alias both DataFrames and select qualified columns afterwards. The output has no ambiguous columns.
- Join keys must have the same type on both sides; cast explicitly first.
- Let adaptive query execution choose broadcast joins. Add `F.broadcast(dim)` only when the plan shows a sort-merge join on a small side and the dimension will stay small.

## Nulls, windows, conditions

- Null-safe equality is `eqNullSafe` (SQL `<=>`). `NOT IN` against a subquery or list containing null returns no rows; use a left anti join.
- `F.when(...)` without `.otherwise(...)` yields null on the remaining rows. Write the `otherwise` when null is not the intended default.
- Every window has an explicit frame (`rowsBetween` or `rangeBetween`) when the result depends on it, and `ignorenulls=True` on `first`/`last` when nulls are possible. Order nulls explicitly (`F.asc_nulls_last`).
- No window with an empty `partitionBy()` and no `Window.orderBy` without `partitionBy`; both move all rows to one task. Use an aggregation.
- Long chains of `when` or nested boolean logic: name the conditions as variables and combine them.

## Built-ins first

Prefer, in order: a built-in function or SQL expression, a higher-order function (`transform`, `filter`, `aggregate` on arrays), a vectorized pandas or Arrow UDF, a Python UDF. Python UDFs serialize every row to Python and cannot run in Photon. Before writing any UDF, name the built-in you looked for (`functions` reference, Spark SQL function list) and why it does not fit.

## The driver is not a worker

- No `collect()`, `toPandas()` or `.rdd` on unbounded data. Small lookups use `limit(n)` first; emptiness checks use `df.isEmpty()`, not `count() > 0`.
- No `show()`, `display()`, `print(df.count())` or `explain()` left in pipeline code; each triggers a job. Measure row counts with `df.observe(...)` or the write's metrics.
- Python loops build plans, not data: a loop over dates that writes once per iteration creates many small jobs and files. Build one DataFrame and write once.
- `cache()` only a DataFrame used by two or more actions, and `unpersist()` it after. Caching a DataFrame used once only adds work.

## Determinism

Re-running a job on the same input must produce the same output.

- Never use `monotonically_increasing_id()`, `rand()` without a seed, `uuid()` or `input_file_name()` as keys; values change between runs and retries. Derive keys from data (`xxhash64` or `sha2` over the natural key columns).
- `current_timestamp()` in a cached or reused DataFrame is evaluated once per action; pass the run timestamp in as a parameter instead.
- Deduplicate with an explicit ordering (`row_number()` over a window ordered by a sequence column), not `dropDuplicates()` on all columns, which keeps an arbitrary row.

## Read when relevant

| Doing | Read |
| --- | --- |
| Reviewing Spark code, or checking a pattern before using it | [references/anti-patterns.md](references/anti-patterns.md) |
| Writing a custom reader or writer with `pyspark.sql.datasource` | [references/python-data-sources.md](references/python-data-sources.md) |

Writing tables, incremental loads, MERGE and pipelines: `building-data-pipelines`. Tests: `testing-pyspark-code`. Slow or expensive jobs: `tuning-spark-jobs`. If the official `databricks-*` skills are installed, use them for product-specific API details; these rules still apply to the code.

## Report

Follow `writing-python-code` for the report. Also state which actions the change adds (writes, counts, collects), any UDF added and the built-in you ruled out, and any join whose key uniqueness you assumed rather than verified.
