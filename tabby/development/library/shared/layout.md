# Package layout

Packages are organized by component; dependencies point one way. Look at the tree before adding a file.

Layout is a map of who may know about whom. Ask where a new piece belongs by what it owns and what depends on it, not by what kind of code it is; a circular import is the map telling you a boundary is in the wrong place.

- Name packages for what they own (`billing/`, `ingest/`, `auth/`), never for the shape of the code (`models/`, `utils/`, `common/`, `misc/`, `base/`).
- A component is a subpackage with its own `__init__.py` and tests that mirror it. Nest only when a package has distinct components, to about three levels below the source root.
- Each package has a public face: its `__init__.py` re-exports what others may use, and other packages import from it, not from internal modules. Layers point one way (`api` to `services` to `domain`); a circular import means the boundary is in the wrong place, so move the boundary instead of hiding the import inside a function.
- Shared types live in a leaf package that imports nothing internal.
- One primary concept per module. Name files for their contents, without repeating the package name. A module past a few hundred lines is a signal to split by concept.
- **Each fact has one home**: the version, the dependency list, a schema, a default config value. Other files read or link to it. The version lives in `pyproject.toml`; code that needs it uses `importlib.metadata.version("<pkg>")` instead of a second literal.
- Give each kind of content one home: docstrings for API behavior, the README for install and usage, `docs/` for concepts, commit messages for history, config comments for config.
- Never hand-edit generated files; edit the source and regenerate. A new top-level directory needs a reason. Update an architecture file if one exists; do not create one unasked.
