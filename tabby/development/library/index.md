# Library

- shared/: any package others import: API, setup, layout, tooling, versions, release.
- smells.md: public API mistakes: positional booleans, leaking internals, breaking a minor release, heavy dependencies. Read for any library.
- native/: Rust or C behind a Python API (`native/smells.md` lists its mistakes).
