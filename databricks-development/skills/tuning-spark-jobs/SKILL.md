---
name: tuning-spark-jobs
description: "Diagnoses slow or expensive Spark and Databricks jobs from evidence: query plans, Spark UI or query profile, skew, spill, shuffle, small files, data skipping, Photon and compute choice, cost attribution. Use when a job, query or pipeline is slow, runs out of memory, or costs too much."
argument-hint: "[runtime=18 compute=serverless]"
---

# Tuning Spark jobs

Measure, change one thing, measure again. Most slow jobs read too much, shuffle too much, or run row-by-row Python; config tweaks rarely beat fixing those.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`compute`, `runtime`, `serverless.environment_version`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts.

- `compute=serverless`: there is no Spark UI and most Spark configs are rejected. Use the query profile and query history; tune the code and the table layout, not the cluster.
- Never change production job compute, schedules or table layout without approval. Report the evidence and the proposed change.

## Get evidence first

1. The plan: `df.explain(mode="formatted")` or `EXPLAIN FORMATTED <query>`. Look for full scans (no pushed filters, no file skipping), `BroadcastNestedLoopJoin` or `CartesianProduct`, `SortMergeJoin` on a small side, Python `BatchEvalPython`/`ArrowEvalPython` nodes, and operators Photon could not run.
2. The run: query profile (serverless, SQL warehouses) or Spark UI stages (classic). Per stage: input size, shuffle read/write, spill, and task duration max vs median.
3. The table: `DESCRIBE DETAIL` (file count, size, clustering columns) and `DESCRIBE HISTORY` (recent operations and their metrics).

State the bottleneck in one sentence, with the number that shows it, before changing anything.

## Symptom to cause

| Evidence | Likely cause | Fix |
| --- | --- | --- |
| Bytes read far above what the query needs | No filter pushdown or file skipping | Filter early on clustering columns; select only needed columns; cluster the table on the filter columns (`designing-delta-tables`) |
| Thousands of tiny files, slow listing | Small-file writes, write-in-loop, streaming without compaction | Optimized writes and auto compaction (default on Databricks for most writes), `OPTIMIZE`, predictive optimization; write once per job |
| One or a few tasks far slower than the median | Skew on a join or group key | Keep AQE skew join handling on; filter or separate null/hot keys; pre-aggregate before the join; salting only as a last resort |
| Large shuffle on a join with a small table | Broadcast not chosen | Check the small side's size estimate (`ANALYZE TABLE ... COMPUTE STATISTICS`); AQE converts at runtime; hint `broadcast()` only when stable and measured |
| Spill to disk, executor OOM | Wide shuffles on too few partitions, huge rows, exploding joins | Fix the join cardinality first; on classic, larger memory per core or more partitions; avoid `collect` |
| Driver OOM | `collect`, `toPandas`, broadcast of a large table, huge plans from loops | Remove the driver pull; build plans without per-column loops |
| Python UDF nodes dominate time | Row-at-a-time Python | Built-in functions; else a pandas or Arrow UDF |
| Same data recomputed in several actions | Missing reuse | One action, or `cache()` + `unpersist()`, or write an intermediate table |
| Stream falls behind | Batch too large or too slow, state growth | `maxFilesPerTrigger`/`maxBytesPerTrigger`, watermarks, RocksDB state store on classic |

Rules for config: keep adaptive query execution on; leave `spark.sql.shuffle.partitions` unset (on classic Databricks, `auto` lets the platform size it); never disable broadcast joins globally. A config change needs the before and after numbers.

## Photon

Photon accelerates built-in SQL and DataFrame operators. Python UDFs, RDD code and a few functions fall back to the slower engine; the plan and query profile show which operators did not run in Photon. Photon pays off for scan-, join- and aggregation-heavy jobs; for jobs dominated by Python or tiny data it adds cost without benefit.

## Compute and cost

- Jobs run on job compute or serverless, never on all-purpose (interactive) clusters, which bill at a higher rate.
- Serverless suits spiky or short jobs and removes cluster tuning; classic job clusters suit long steady runs, custom Spark configs, RDD or Scala code. Compare with real runs, not list prices.
- Streams that need minutes of latency run as scheduled `availableNow` jobs, not 24/7 clusters.
- Attribute cost with tags on jobs and pipelines and query `system.billing.usage` joined to `system.billing.list_prices`; find the expensive jobs before tuning cheap ones.
- Static checks catch known cost anti-patterns before they run: `burnt check` if the project uses burnt, and the patterns in `writing-pyspark-transformations` (`references/anti-patterns.md`).

## Verify

Rerun on the same input and compare duration, bytes read, shuffle and cost; check the output is identical (`assertDataFrameEqual` or a row-count and checksum comparison). Report before and after numbers, the change, and anything you suspect but did not measure.
