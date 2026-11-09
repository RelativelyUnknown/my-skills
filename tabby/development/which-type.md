# Which kind of project

Read once per project. Save the matching paths, comma-separated, as `kind:` in the AGENTS.md defaults. Paths are under `development/`. A path with no folder is not built: use `code` and say so.

- `[project]` with a build backend and `src/`; others import it: `library/shared`
- `[project]` plus `Cargo.toml` (maturin), `ext_modules`, `CMakeLists.txt`, `meson.build` or `.pyx` files: `library/native`
- FastAPI, Django REST, Flask JSON or similar HTTP service: `application/apis/http`
- A queue client, worker or scheduler: `application/workers`
- Async handlers, caches, other service code: `application/shared`
- A question about boundaries, patterns, layers or extension points: `architecture`
- Anything else, or unsure: `code`
