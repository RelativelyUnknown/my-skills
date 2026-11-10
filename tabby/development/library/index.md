# Library

- shared/: any package others import: API, setup, layout, tooling, versions, release. For a library read `smells.md`, then `shared/package-setup.md`, `layout.md`, `versioning.md`, `release.md`, and `shared/api-design.md` for any public name.
- smells.md: public API mistakes: positional booleans, leaking internals, breaking a minor release, heavy dependencies. Read for any library.
- native/: Rust or C behind a Python API (`native/smells.md` lists its mistakes).
