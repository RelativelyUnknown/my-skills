---
name: designing-delta-tables
description: "Designs and maintains Delta tables in Unity Catalog: managed vs external, liquid clustering vs partitioning, table properties, constraints, comments, schema evolution, OPTIMIZE/VACUUM, predictive optimization, grants. Use when creating or altering a table, choosing clustering keys, or changing retention or maintenance."
argument-hint: "[runtime=18 compute=serverless]"
---

# Designing Delta tables

A table is an API for everyone downstream. Its name, grain, key, columns and history are promises; design them on purpose and change them deliberately.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`runtime`, `compute`, `bundle.targets`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Features below name their minimum Databricks Runtime; check `runtime` before using one.

Dropping or replacing a table, removing or renaming columns, changing clustering on a large table (`OPTIMIZE FULL` can run for hours), protocol upgrades, retention changes and `RESTORE` need approval. Protocol upgrades cannot be undone and can lock out older readers.

## Defaults for a new table

- **Unity Catalog managed table**, addressed as `catalog.schema.table`. External tables only when another system must own the files or the location is mandated; predictive optimization and automatic clustering work only on managed tables.
- **No partitioning.** Use liquid clustering: `CLUSTER BY (col, ...)` with at most four columns, chosen from the columns queries filter on most, dropping one of any two highly correlated columns. Or `CLUSTER BY AUTO` (DBR 15.4 LTS+, managed tables, predictive optimization on) to let Databricks choose and change keys. Clustering cannot be combined with `PARTITIONED BY` or `ZORDER`.
- **Predictive optimization** runs `OPTIMIZE`, `VACUUM` and `ANALYZE` on managed tables. Check with `DESCRIBE TABLE EXTENDED`; when it is on, do not add scheduled OPTIMIZE or VACUUM jobs.
- **Explicit schema** with types fit for the data: `BIGINT` keys, `DECIMAL(p,s)` for money, `TIMESTAMP` in UTC, `DATE` for dates, `STRING` for text, `VARIANT` for semi-structured payloads.
- **Comments** on the table (grain, key, source, owner, refresh cadence) and on every column whose meaning is not obvious. Catalog explorers, lineage and AI assistants read them.

```sql
CREATE TABLE IF NOT EXISTS main.sales.orders (
  order_id     BIGINT        NOT NULL COMMENT 'Source system order ID',
  customer_id  BIGINT        NOT NULL,
  order_ts     TIMESTAMP     NOT NULL COMMENT 'UTC',
  amount       DECIMAL(18,2) NOT NULL,
  status       STRING        NOT NULL,
  CONSTRAINT orders_pk PRIMARY KEY (order_id) RELY,
  CONSTRAINT valid_status CHECK (status IN ('open', 'paid', 'cancelled'))
)
CLUSTER BY (customer_id, order_ts)
COMMENT 'One row per order. Source: shop CDC feed. Owner: data-eng. Refreshed hourly.'
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');
```

## Keys and constraints

- `NOT NULL` and `CHECK` constraints are enforced on write: a violating batch fails. Use them for invariants that must never break.
- `PRIMARY KEY` and `FOREIGN KEY` are informational, not enforced. Declare them for documentation and lineage; add `RELY` only when the pipeline guarantees uniqueness, because the optimizer then trusts it. Enforce uniqueness with a test or a data-quality check.
- Identity columns (`GENERATED ALWAYS AS IDENTITY`) give surrogate keys but disable concurrent transactions on the table, and values differ when a load is replayed; a hash of the natural key suits idempotent loads better.

## Properties worth choosing

| Property | Set when |
| --- | --- |
| `delta.enableChangeDataFeed = true` | Downstream needs row-level changes (incremental silver/gold, CDC out) |
| `delta.deletedFileRetentionDuration` | Time travel or slow readers need more than the 7-day default; set before relying on predictive VACUUM |
| `delta.logRetentionDuration` | History must be queryable beyond the default 30 days |
| `delta.columnMapping.mode = 'name'` | Columns will be renamed or dropped, or names contain spaces or special characters |
| `delta.enableTypeWidening = true` | Numeric or date types are expected to widen without a rewrite |
| `delta.enableRowTracking = true` | Row-level concurrency or incremental materialized-view refresh needs it |

Deletion vectors are on by default on current runtimes; leave them on (turning them or row tracking off disables row-level concurrency and raises conflict rates).

## Changing a table

- Add columns with `ALTER TABLE ... ADD COLUMN` in the deployment, or `mergeSchema` on the single write that introduces them. Never enable schema auto-merge for the whole session.
- Rename or drop columns only with column mapping on, after checking every consumer; it is a breaking change for readers.
- Change clustering keys with `ALTER TABLE ... CLUSTER BY (...)`; existing files are reclustered by later `OPTIMIZE` runs, or at once with `OPTIMIZE FULL` (DBR 16.0+). Convert a partitioned table with `REPLACE PARTITIONED BY WITH CLUSTER BY` on DBR 18.1+, otherwise rebuild it with `CREATE TABLE ... CLUSTER BY ... AS SELECT`.
- Prefer `CREATE OR REPLACE TABLE` to drop-and-create: history survives for time travel, and concurrent readers never see a missing table.

## Maintenance without predictive optimization

- `OPTIMIZE` incrementally on clustered tables (every one or two hours for heavily written ones); `ZORDER BY` only on legacy, non-clustered tables.
- `VACUUM` with the default 7-day retention or longer. Never set `spark.databricks.delta.retentionDurationCheck.enabled = false`; readers and streams still using old files will fail or lose data.
- Recover from a bad write with time travel: query `VERSION AS OF`, then `RESTORE TABLE ... TO VERSION AS OF n` (needs approval).

## Governance

- Grant to groups, never to individual users: `GRANT SELECT ON TABLE main.sales.orders TO \`analysts\``. Readers also need `USE CATALOG` and `USE SCHEMA`.
- Sensitive columns: row filters and column masks, or a separate restricted table, not a view nobody maintains.
- Files go in Unity Catalog volumes (`/Volumes/catalog/schema/volume/...`), not DBFS root or mounts. Checkpoints and schema locations too.
- Tag tables and columns (`ALTER TABLE ... SET TAGS`) for ownership, sensitivity and cost attribution when the organization uses tags.

## Naming

- Snake case, singular or plural consistently, no environment in the table name. Environment and layer live in the catalog or schema (`dev_sales.silver.orders`), set by bundle variables.
- Name for the business entity and grain (`orders`, `daily_revenue_by_store`), not the job that writes it.

## Report

List every table created or altered with its DDL, every property or protocol change, every operation that needed approval and whether it ran, and the clustering choice with the queries it serves.
