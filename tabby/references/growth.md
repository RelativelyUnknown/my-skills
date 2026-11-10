# Growth: build the seam, not the feature

`growth:` in the `## Tabby` section is the one exception to "no speculative generality". For each item, build only the cheap seam that keeps the change small later. A seam costs about one file or one parameter, and a test exercises it. The feature stays unbuilt until a task asks for it.

| Growth item | Build now | Leave unbuilt |
| --- | --- | --- |
| A hot path may move to Rust or C | The function behind one module with a fully typed signature and a pure-Python implementation; one import site; a test that runs the reference on real inputs; a recorded benchmark | Cargo workspace, maturin, wheels, C sources |
| A public API others will depend on | `__all__`, flat imports, `py.typed`, one root exception, the version in one place, keyword-only options ([api-design.md](../development/library/shared/api-design.md)) | A plugin system, registries, deprecation machinery |
| It may become a service | Core logic as functions that take values (including time and config); a thin outer layer that reads the clock, environment and network | A web framework, auth, a database layer |
| More integrations or data sources | One `Protocol` at the single seam where sources differ; one settings object | An adapter per imagined source: write the second one when it exists |
| More users or scale | Idempotent handlers, timeouts, bounded queues and batches; a profile before any speed-up | Caching, sharding, async everywhere |
| A second platform or Python version | The target in the CI matrix; platform checks in one module | Platform branches across the code |
| Others will contribute | The canonical check command in `commands:`; CONTRIBUTING with that command | Governance documents beyond that |

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
