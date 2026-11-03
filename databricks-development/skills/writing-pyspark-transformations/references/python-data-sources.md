# Python data sources (`pyspark.sql.datasource`)

Spark 4.0 (and Databricks Runtime 15.x and up, which shipped it early) lets you write batch and streaming readers and writers in Python. Use one when no built-in connector, Lakeflow Connect connector or JDBC/federation route exists. Check the PySpark API reference for your runtime's version before using newer hooks such as filter pushdown.

## Shape

| Need | Implement on `DataSource` | Returns |
| --- | --- | --- |
| Batch read | `reader(schema)` | `DataSourceReader` with `read(partition)` and optional `partitions()` |
| Batch write | `writer(schema, overwrite)` | `DataSourceWriter` with `write(rows)`, `commit(messages)`, `abort(messages)` |
| Streaming read | `streamReader(schema)` | `DataSourceStreamReader`: `initialOffset`, `latestOffset`, `partitions(start, end)`, `read`, `commit` |
| Simple streaming read | `simpleStreamReader(schema)` (used only without `streamReader`) | `SimpleDataSourceStreamReader`: `read(start)`, `readBetweenOffsets` |
| Streaming write | `streamWriter(schema, overwrite)` | `DataSourceStreamWriter` |

`name()` is a classmethod returning the format name; `schema()` returns a `StructType` or DDL string. Register with `spark.dataSource.register(MySource)`, then `spark.read.format("my_source")`.

## Rules

- Everything is pickled to executors: the source, reader and writer classes and their state. Keep state to plain values (options, schema); open clients inside `read`/`write`.
- Import third-party libraries inside the method that uses them, not at module top, so the driver object stays picklable and executors import what they need.
- Options arrive as strings. Parse and validate them once in the `DataSource` constructor or `reader`, and raise with the option name and accepted values.
- Partition the work: `partitions()` returns `InputPartition` objects (page ranges, ID ranges, files) so executors read in parallel. One partition means one task.
- Yield `pyarrow.RecordBatch` objects instead of tuples for large reads; the PySpark docs report up to an order of magnitude speedup.
- Streaming: offsets are JSON-serializable dicts; the end offset must advance whenever data is returned; return the start offset and an empty iterator when there is nothing new. Implement `getDefaultReadLimit` and honor the limit in `latestOffset` to cap batch sizes. `readBetweenOffsets` must be deterministic so a failed batch replays the same rows.
- Writers: `write` returns a `WriterCommitMessage`; make `commit` the only place results become visible, and make `abort` clean up partial output.
- Pick a format name that no built-in or JVM source uses; built-ins win name conflicts, and re-registering a name overwrites the earlier source.
- Credentials come from a secret scope or a Unity Catalog connection passed in as an option at the call site, never from code.

## Testing

- Unit-test the pure parts (option parsing, offset arithmetic, row conversion) without Spark.
- Integration-test with a local `SparkSession`: register the source, read a small fake backend (a local HTTP server or a temp directory), and compare with `assertDataFrameEqual`. Assert the partition count and that a second read with the same offsets returns the same rows.
- Mark tests that hit a real external system and keep them out of the default run.
