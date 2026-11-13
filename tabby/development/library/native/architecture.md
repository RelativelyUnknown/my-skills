# Native architecture

## Go native only on evidence

Native code is a standing cost: a compiler in the build, a wheel matrix, and an interface that moves with each Python release. Before starting:

1. Profile. Name the function and its share of the run time ([performance](../../performance/index.md)).
2. Call frequency decides. A 200 ns Python function called once per input gains nothing from a 50 ns native one; a tight loop over large data does.
3. Try cheaper first: a better algorithm, `itertools`, NumPy vectorisation, an existing library ([performance](../../performance/index.md)). I/O-bound work needs `asyncio`, not native code.
4. Record the benchmark and the decision (an ADR or a code comment): "X was 70% of the run at N calls per second."

## Choose the layer

| Need | Use |
| --- | --- |
| Call an existing C library, no new code | `cffi` (or `ctypes` for coarse calls) |
| Existing C++ library | `nanobind` (new work) or `pybind11` (existing code) |
| New safe, fast module | Rust with PyO3 and maturin |
| Python-shaped numeric loops | Cython |
| A tiny, stable kernel in C | The raw C API, accepting the maintenance |

Rust is usually the better choice for new native code: the compiler removes most reference-count and memory bugs that the raw C API leaves to you.

## Layout

Four shapes occur in widely used packages. Pick the smallest that fits, and keep one rule across all of them: native code sits behind one private module, and a typed Python package sits in front.

1. **Binding in the package** (pydantic-core, orjson): `src/` holds Rust, `python/<pkg>/` holds the Python package with `py.typed` and a `.pyi` stub for the native module. maturin builds both.
2. **Core crate plus binding crate** (polars, cryptography, uv): logic lives in Rust crates that do not depend on PyO3; one small crate holds the bindings. Several small, flat crates beat one big crate. Use this when the core may be reused from Rust or tested without Python.
3. **A binary shipped on PyPI** (uv, ruff): maturin with `bindings = "bin"` and a thin Python shim that finds the executable.
4. **C or Cython extension** (pandas, numpy, msgspec): native sources in one directory (`pandas/_libs/`, `src/msgspec/`), built with Meson, scikit-build-core or setuptools.

## The seam and the fallback

- The Python call site imports from one place. Keep a pure-Python implementation of the same function as the reference. Tests run both and compare results on the same inputs; the fallback also serves PyPy and installs with no compiler.
- A missing accelerator must be visible: `try: from ._native import f` then `except ImportError:` import the reference and log once at debug level. Never `pass` the `ImportError`.
- The public API stays typed and Pythonic: `py.typed`, a `.pyi` for the native module, stubs checked in CI (`mypy.stubtest`). Native types do not leak into signatures.

## The boundary

- Data layout is a design decision: decide it from the workload and the plans, and record why ([fit.md](../../architecture/fit.md)).

- Convert and validate once at the edge, then work on native types. Avoid per-element round trips: pass whole buffers or batches.
- One owner per allocation; the side that allocates frees. Never hand out a pointer that outlives its owner.
- Errors cross as Python exceptions, never as panics or unhandled C errors (details in rust.md, c.md and cpp.md).
- Release the GIL for long native work; touch Python objects only while holding it.
- Declare free-threaded support only after the module has no unsynchronised shared state, and test it.

## One core, many callers

Seen in TigerBeetle (one Zig core behind clients for six languages) and Ghostty's `libghostty-vt`:

- **A thin ABI.** A handful of functions: init, submit, deinit. The caller owns the handle, so no allocation crosses the boundary; results are valid only inside the completion callback; awkward values (128-bit integers) travel as byte arrays or halves, not by value. The binding turns status codes into typed exceptions in one place.
- **One definition generates the rest.** The C header and the Python bindings are generated from the core's types, and CI regenerates and fails if a checked-in file is stale. A parity test compares header and binding sizes, offsets and enum values.
- **Guard the ABI.** Opaque handles read and changed through getters and setters keyed by an enum, so a new property is a new enum value, not a new symbol or struct field; enums pinned to `int`; sized structs and reserved fields; a committed symbol list and ABI baseline that fail on any non-additive change; compile the public header as C11, C23 and C++17 with warnings as errors.
- **Write conformance cases once** and emit tests for each language. Run the README samples in CI, test the published package (a fresh install in a clean environment), and run `mypy --strict` on the binding.
- **Data that crosses the boundary** is one contiguous block addressed by offsets, not pointers, so it can be copied or handed over; zero is a valid empty state; capacity is fixed and the caller decides how to grow it; a generation number on each handle catches a stale one.

