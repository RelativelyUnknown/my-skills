# Zig behind a Python API

Zig is a smaller choice than Rust or C for a Python extension, with far less real-world track record and a 0.x language that still breaks between releases; pick it only when the project already uses Zig, or when its `comptime` and explicit-allocator model are the point. For most new native code, prefer Rust ([rust.md](rust.md)).

## Ziggy Pydust

[Ziggy Pydust](https://github.com/fulcrum-so/ziggy-pydust) is the maintained framework for this: it generates the CPython module boilerplate from plain Zig functions and structs, with `comptime` argument wrapping and unwrapping between Python objects and native Zig types. At the time of writing it supports Zig 0.14.0 and CPython 3.11 and later; check both versions against the installed toolchain before relying on an example.

- **Build.** A `build.zig` builds the extension with `zig build`, locating the Python include path, library path and ABI version from the interpreter at build time (`python-config`-style probing); there is no separate C compiler step.
- **Module definition.** `comptime { py.rootmodule(@This()); }` at the bottom of a file turns its public functions into the module's Python-visible API. Arguments are a Zig `struct` with named fields, matching Python's keyword arguments; Pydust generates the parsing and conversion code.
- **Tests.** A pytest plugin (`pydust.pytest_plugin`) discovers Zig test blocks and runs them through `pytest`, so native tests sit in the same `pytest` run as the Python suite.

## What to carry over from Rust and C

Same shape as [rust.md](rust.md) and [c.md](c.md), adapted to Zig's own tools:

- **Memory.** Zig has no borrow checker; every allocation takes an explicit `std.mem.Allocator`, so ownership is a parameter you choose, not inferred. Pick the allocator deliberately (an arena for a request's lifetime, the general-purpose allocator elsewhere) and free on the same side that allocated, as in C.
- **Errors.** Map Zig's error unions (`!T`) to Python exceptions at the module boundary; never let a Zig `error` or a `@panic` cross into Python unconverted.
- **Safety checks.** Zig's `ReleaseSafe` build mode keeps bounds and overflow checks in a build that is still fast; use it for the extension's release build rather than `ReleaseFast`, which strips them, unless a profile shows the checks themselves are the bottleneck.
- **Boundary review.** The checklist in `review/native-boundary.md` (reference counts, error translation, buffer lifetime, layout) applies the same way; only the per-language syntax differs.
