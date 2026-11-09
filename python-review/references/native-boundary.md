# Reviewing a native extension boundary (Rust, C, C++ with Python)

Use with `security-audit/process.md` when the change crosses between Python and native code. A finding needs a concrete input or call sequence; no case, no finding. Static reading is enough to report `needs-validation`; `confirmed` needs a run (a failing test, a sanitizer trace, a crash).

## 1. Build the boundary table first

One row per exported function, callback or buffer. Most native bugs are one disagreement in this table.

| Function | Accepts (length, type, null, negative) | Checked how | Allocated by | Freed by | Thread / GIL | On error |
| --- | --- | --- | --- | --- | --- | --- |

Then ask of every row:

- Does the check use the same unit as the allocation and the copy (bytes, elements, code units)?
- Is the worst accepted size safe: overflow in `count * size`, a negative `Py_ssize_t`, a 64-bit length narrowed to 32?
- Does the pointer outlive its owner, including after a callback, a cancellation or a close?

## 2. Reference counts and errors (C API, Cython)

- Each call: new or borrowed reference? A borrowed one held across a call that can run Python code is a use-after-free.
- Every error path: references released once, none twice; `NULL` returned with an exception set; no exception left set on success.
- Unchecked fallible calls (`PyList_GetItem`, `PyLong_AsLong` with `-1`, allocations, `PyUnicode_AsUTF8`).
- `tp_clear` frees memory instead of breaking references; GC type missing `tp_traverse`; tracked object freed with `PyObject_GC_Del`.
- `PyObject_GetBuffer` without `PyBuffer_Release`.

## 3. Rust and PyO3

- `unwrap()`, `expect()`, indexing or `as` casts reachable from Python input; a panic crossing the boundary.
- `unsafe` without `// SAFETY:`; an `unsafe fn` without `# Safety`; `unsafe impl Send` or `transmute` to quiet the compiler; a safe function that can cause undefined behaviour through safe calls.
- A Python object kept past the call without `Py<T>`; GIL released while touching Python objects; a lock guard held across a call back into Python.
- Errors mapped to the wrong exception or with the cause dropped.
- `#[pymodule(gil_used = false)]` claimed with shared mutable state.

## 4. Layout and ABI

- Struct, enum and integer widths that differ by platform; `#[repr(C)]` missing on a shared struct.
- Exceptions or panics unwinding through an ABI that forbids it; callbacks run after the module is torn down; an API that needs one thread called from another.
- A module that claims `abi3` using a non-limited API symbol; a wheel tag that does not match what was built.

## 5. Tests and tools to ask for

- Sanitizer run (ASan, UBSan, TSan for threads), Miri for Rust `unsafe`, a Python debug build, a 10,000-call leak loop.
- A test for each error path, and for empty, maximum and negative sizes.
- A fuzz target for any parser of untrusted bytes.
- The pure-Python reference compared against the native result.

## Report

Use the confirmed / needs-validation / rejected split from `security-audit/reporting.md`. For each finding: where (`file:line`), the rule broken, the failing input or call, the smallest fix, and the regression test. Say which of the sanitizer, Miri or test runs you did not perform.
