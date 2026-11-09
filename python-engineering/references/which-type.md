# Which kind of project

Read once per project. Save the matching paths, comma-separated, as `kind:` in the AGENTS.md defaults. Paths are under `references/fields/`. A path with no folder is not built: use `software-engineering/all` and say so.

- `[project]` with a build backend and `src/`; others import it: `software-engineering/library/shared`
- FastAPI, Django REST, Flask JSON or similar HTTP service: `software-engineering/application/apis/http`
- A queue client, worker or scheduler: `software-engineering/application/workers`
- Async handlers, caches, other service code: `software-engineering/application/shared`
- A question about boundaries, patterns, layers or extension points: `software-architecture`
- Anything else, or unsure: `software-engineering/all`
