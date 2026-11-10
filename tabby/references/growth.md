# Options and seams: think past the ask

Read this when a request adds a layer or a choice that is hard to undo (an API, a queue, a cache, auth, an ORM, async, a new store), or when `growth:` names something that may come. A senior engineer decides with what the project is and where it is going, builds what was asked today, and builds it so the next step is cheap. `growth:` in `## Tabby` is the one exception to "no speculative generality": build the seam, not the feature.

## 1. Read the evidence

How the code reaches its data today (plain parameterised SQL, a query builder, an ORM); how many entities and relationships; the shape of the queries (joins, filters, writes); whether the driver is sync or async; who calls it and how often; the deployment. In `## Tabby`: `growth:` and `workload:` (read or write heavy, rough rates, concurrency, data size). With no section, infer from the code and ask the one question that would change the decision most ("is a second client or more than one customer coming?") in the same message as the work.

## 2. Two or three options for each real fork

Name them, the criterion that decides, and what this project's evidence says. Candidates come from [ecosystem.md](../development/ecosystem.md) and the ladder in [reuse.md](../development/code/reuse.md); check installed and current versions before recommending one. Examples of the criteria:

- **Data access:** keep plain SQL when there are few tables and a handful of hot queries; a query builder when filters are built dynamically; an ORM when there are many related entities, schema change is frequent, migrations matter or several clients share the model.
- **Sync or async:** async pays when many requests wait on I/O at once and the driver is async. A sync driver or CPU-bound work gains nothing.
- **Caching:** when reads dominate, are expensive and may be stale for a stated time. After a measurement, not before.
- **A queue:** when work must survive a restart or outlast a request.

## 3. Choose for today, make the next one cheap

| Growth item | Build now | Leave unbuilt |
| --- | --- | --- |
| A hot path may move to Rust or C | The function behind one module with a fully typed signature and a pure-Python implementation; one import site; a test that runs the reference on real inputs; a recorded benchmark | Cargo workspace, maturin, wheels, C sources |
| A public API others will depend on | `__all__`, flat imports, `py.typed`, one root exception, the version in one place, keyword-only options ([api-design.md](../development/library/shared/api-design.md)) | A plugin system, registries, deprecation machinery |
| It may become a service | Core logic as functions that take values (including time and config); a thin outer layer that reads the clock, environment and network | A web framework, auth, a database layer |
| An ORM later | Data access in functions that take a connection and return typed rows; no SQL in handlers or views; one place builds connections | An ORM, a model layer, a migration tool |
| Async later | I/O at the edges, a pure core, no module-level state; handlers that only parse, call and return | Async drivers, an async rewrite of the core |
| A cache later | Read functions that depend only on their arguments (no hidden clock or global); one function to wrap | A cache layer, invalidation rules |
| Auth later | One dependency or middleware slot every route passes through; the user id passed explicitly to data access | An auth system |
| Several tenants later | A tenant id in every data-access signature | Tenant routing, row-level security |
| More clients later | Response models separate from storage rows; a versioned path prefix | A versioning scheme beyond that |
| More integrations or data sources | One `Protocol` at the single seam where sources differ; one settings object | An adapter per imagined source: write the second when it exists |
| More users or scale | Idempotent handlers, timeouts, bounded queues and batches; a profile before any speed-up | Caching, sharding, async everywhere |
| A second platform or Python version | The target in the CI matrix; platform checks in one module | Platform branches across the code |
| Others will contribute | The canonical check command in `commands:`; CONTRIBUTING with that command | Governance documents beyond that |

A seam costs about one file or one parameter and a test exercises it.

## 4. Say it once

In the reply, briefly: what you found in the project, the options and why you chose this one, what you kept open, and what would make you change it. Go ahead with the recommended option when it is cheap to change because of the seams. Stop and ask first when it binds data or a public contract: a schema or ORM migration, a public API shape, a costly dependency.

## When an item becomes real

1. Re-read `out-of-scope:` and `constraints:`. Ask if the task conflicts.
2. Read the leaf for that kind of work: `development/library/native/index.md` for a first Rust, C or C++ module (`porting.md` to move an existing function), `development/application/apis/http/services.md` for a first endpoint, `development/library/shared/api-design.md` for a first public release.
3. For a first data structure, representation or algorithm choice, read `development/architecture/fit.md`.
4. Write one ADR (`documentation/history/adr.md`): the decision, the alternatives, what would change it.
5. Move the item from `growth:` to `goals:` or delete it. Update `reviewed:`.

## Smells

- A seam with no test, or with one implementation and no stated growth item behind it: delete it.
- More than three seams for one item: the item is too vague; ask what the first concrete step is.
- A `growth:` item older than a year with no movement: ask whether it is still true.
- A choice presented as the only option: name the one you rejected and why.
