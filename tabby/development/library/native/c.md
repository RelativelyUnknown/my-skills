# The CPython C API

Prefer something else first ([architecture.md](architecture.md)): Rust, Cython, `cffi` or `nanobind` remove most of what follows. Use the raw API for a small, stable kernel, and expect to maintain it across Python releases. Style: PEP 7 and the project's `.clang-format` (4-space indent, braces on every block); `-Wall -Wextra -Werror`.

## Every function

- Returns a **new reference** or `NULL` with an exception set (or `-1` for `int` returns). Returning `NULL` with no exception, or a value with an exception still set, are both bugs.
- Know for each API call whether it returns a new or a borrowed reference. A borrowed reference (from `PyList_GetItem`, `PyTuple_GetItem`, `PyDict_GetItem`) can dangle after any call that may run Python code. Take a strong reference at once with `Py_INCREF`, or use `PyList_GetItemRef` and `PyDict_GetItemRef` (3.13+).
- Check every fallible call: allocations, `PyUnicode_AsUTF8AndSize`, `PyObject_GetAttr*`, item getters. After `PyLong_As*`, a result of `-1` needs `PyErr_Occurred()`.
- One cleanup path: initialise every owned local to `NULL`, `goto error` on failure, release with `Py_XDECREF` or `Py_CLEAR`.
- Sizes are `Py_ssize_t`. Reject negatives before casting to `size_t`, and check for overflow before multiplying or adding sizes that come from input.

## Types and the garbage collector

- A type with `Py_TPFLAGS_HAVE_GC` needs `tp_traverse` and `tp_clear`. `tp_clear` only breaks references (`Py_CLEAR`), may run more than once, and frees no memory; `tp_dealloc` frees. Call `PyObject_GC_UnTrack` first in dealloc.
- Heap types decrement the type reference in dealloc. Never release a tracked GC object with `PyObject_GC_Del` instead of `Py_DECREF`.

## Module, threads, buffers

- Multi-phase init (`Py_mod_exec`) and per-module state; no mutable globals.
- Free-threaded builds: declare `Py_mod_gil` with `Py_MOD_GIL_NOT_USED` only after making shared state thread safe; otherwise the GIL comes back on import.
- `Py_BEGIN_ALLOW_THREADS` around long blocking work, and touch no Python object until `Py_END_ALLOW_THREADS`.
- Every successful `PyObject_GetBuffer` is paired with `PyBuffer_Release`; never assume contiguity or format you did not request.
- Guard version-specific code with `PY_VERSION_HEX`. The old `Py_UNICODE` APIs are gone since 3.12.
- Stable ABI: define `Py_LIMITED_API`, use only limited-API calls, and build an `abi3` wheel.

See also [senior-engineering.md](../../architecture/senior-engineering.md) for how large C and Rust codebases confine unsafe memory access.

## The C core behind the binding

Keep the logic in plain C with no Python headers, and make the binding a thin layer over it, so the core is testable on its own. A working example with tests is in [assets/native/c_core/](../../assets/native/c_core/) (`make test` builds it under ASan and UBSan).

- Every allocation has one owner and one place that frees it. Work whose results share a lifetime allocates from an arena and frees it once; a fixed-capacity arena keeps handed-out pointers valid.
- Bytes travel as pointer plus length (a span). Never depend on a terminating NUL: input can contain one, and a view needs no copy.
- Check a size multiplication and an alignment round-up for overflow before trusting either, and report overflow differently from out-of-memory.
- Return a status and write results through out-parameters; a library never calls `abort` or `exit`. The binding turns the status into an exception.
- Compile the core with `-Wall -Wextra -Werror`; run its tests under the sanitizers.

## Testing

- Build with ASan and UBSan (`-fsanitize=address,undefined`) and run the suite; a Python debug build (`--with-pydebug`) or `python -X dev` with `PYTHONMALLOC=debug` catches refcount and allocator misuse.
- Leak test: call the function 10,000 times and compare memory (`tracemalloc`) or `sys.getrefcount` of an argument before and after.
- Fuzz parsers of untrusted bytes (libFuzzer or AFL++). Test every error path, not only success.
- Run the same inputs through the pure-Python reference and compare.

Reviewing someone else's C extension: `native-boundary.md` in the `tabby-review` skill (`../tabby-review/`).
