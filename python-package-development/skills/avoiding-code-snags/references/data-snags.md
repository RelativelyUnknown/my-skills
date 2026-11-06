# Data code snags (pandas, PySpark, SQL)

Same severity scale as `SKILL.md`. Platform-specific rules (Delta tables, pipelines, tuning) live in the Databricks skills (`writing-pyspark-transformations`, `tuning-spark-jobs`, `designing-delta-tables`) if they are installed; this list is only for recognizing the snag.

| Snag | Looks like | Fix |
| --- | --- | --- |
| Secret in code (blocker) | `TOKEN = "dapi..."`, a password in a job parameter | secret scope or the platform's identity |
| Non-idempotent load (blocker) | `mode("append")` that duplicates rows when the job is re-run | merge on a key, or overwrite the partition for that run |
| SQL built per row (blocker) | an f-string `DELETE ... WHERE id = {i}` in a loop | one set-based statement with parameters |
| Whole table to the driver (blocker) | `df.toPandas()`, or `collect()` to drive control flow | aggregate or filter first; `limit(n)` for a sample |
| Row loop (wince) | `iterrows()`, `itertuples()` over a large frame | vectorized expression, or `merge` |
| Row-wise apply (wince) | `df.apply(lambda r: ..., axis=1)`, a Python UDF per row | built-in or column expressions; a pandas UDF if Python is unavoidable |
| Chained assignment (blocker) | `df[mask]["col"] = x` | `df.loc[mask, "col"] = x`; it does nothing, or raises, under Copy-on-Write (pandas 3) |
| `inplace=True` (wince) | `df.fillna(0, inplace=True)` | assign the result: `df = df.fillna(0)` |
| `count()` to test emptiness (wince) | `if df.count() > 0` | `not df.isEmpty()` |
| `select("*")` or `SELECT *` before a join (wince) | | select only the columns used |
| Hard-coded location (wince) | `/mnt/data/...`, a catalog name in the code | a parameter or bundle variable per environment |
| `repartition(1)` (wince) | a single partition for the final write | leave the layout to the engine |
| Business logic in a notebook (wince) | transformations only runnable by running the notebook | a function from a package that takes and returns a DataFrame |

Fine as written: a bounded sample (`limit(1000).toPandas()`), a broadcast of a small dimension table, and `toPandas()` on an aggregated result.
