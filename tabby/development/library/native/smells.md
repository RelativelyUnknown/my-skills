# Native boundary smells (Rust, C or C++ behind Python)

Same format as [code/smells.md](../../code/smells.md): the smell, `→`, the fix. The rules are in [rust.md](rust.md) and [c.md](c.md); the review checklist is `review/native-boundary.md`.

## Rust and PyO3

- `unwrap()`, `expect()`, indexing or an `as` cast reachable from Python input, or a panic crossing the boundary → `?` and `PyResult`; map each error to a Python exception
- `unsafe` with no `// SAFETY:`, or an `unsafe fn` with no `# Safety` section → state why the invariants hold; keep `unsafe` in the smallest module behind a safe API
- `unsafe impl Send` or `transmute` used to quiet the compiler → fix the design
- A Python object kept past the call without `Py<T>`, or the GIL released while Python objects are touched → own the reference; detach only around pure Rust work
- `#[pymodule(gil_used = false)]` with shared mutable state → protect the state and test on a free-threaded build
- A native type in a public Python signature, or a native import with no visible fallback → a typed Python wrapper; on `ImportError` fall back to the reference and log once

## C API

- A borrowed reference held across a call that can run Python code → `Py_INCREF` at once, or `PyList_GetItemRef` / `PyDict_GetItemRef` (3.13+)
- `NULL` returned with no exception set, or a value returned with one set → `NULL` with the exception for object returns, `-1` for `int`
- An unchecked fallible call (item getters, allocations, `PyLong_As*` returning `-1` with no `PyErr_Occurred()` check) → check every one
- References released on some error paths only → one cleanup path: owned locals start `NULL`, `goto error`, `Py_XDECREF`
- Size arithmetic on input without an overflow check, or a negative `Py_ssize_t` cast to `size_t` → check sign and overflow first
- `tp_clear` that frees memory, or a GC type with no `tp_traverse` → `tp_clear` only breaks references; `tp_dealloc` frees
- `PyObject_GetBuffer` with no `PyBuffer_Release` → pair them on every path
- Python objects touched between `Py_BEGIN_ALLOW_THREADS` and `Py_END_ALLOW_THREADS` → none
- A module claiming abi3 that uses a non-limited symbol, or `Py_MOD_GIL_NOT_USED` declared without thread-safe state → limited API only; declare it after the state is safe

## Both

- No sanitizer, Miri or leak-loop run, and no pure-Python reference to compare against → run them and keep one
