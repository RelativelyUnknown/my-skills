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

## 2b. C and C++ habits that become extension bugs

For each size, index or length that crosses from Python, count the sites that use it and account for every one; a bug found in a function does not mean the rest of it is clean. Read the cold error paths on purpose, because they are where leaks and missing frees sit.

- `snprintf` returns the length the output would have had: `buf[n] = 0`, `ptr += n` or `size - n` with that value goes out of bounds or negative (checked: a 16-character string into 8 bytes returns 16). `strncpy` does not terminate when the source fills the buffer (checked); `strncat` counts bytes to append, not the destination size.
- A negative return (`read`, `recv`, `snprintf`) stored in a `size_t` becomes `SIZE_MAX` (checked), and a later `n == -1` is never true. Unsigned subtraction that can go below zero wraps (checked: `0u - 1` is 4294967295) and passes every upper-bound test. `n * sizeof(T)` and `a + b` need an overflow check before the allocation or the comparison, and a signed-overflow check written after the fact may be deleted by the compiler.
- `realloc` leaves every other copy of the old pointer dangling; `malloc` does not zero; a struct with padding written to a socket or file leaks stack bytes; an out-parameter on an early-error return is left uninitialised; `memset` on a secret just before the buffer dies can be optimised away (`explicit_bzero`, `memset_s`).
- A null check after the dereference may be removed; `assert` vanishes under `NDEBUG`; shifts by the type's width or more, misaligned casts and strict-aliasing violations are undefined, not merely wrong.
- `errno` is only meaningful after a failure and is overwritten by the logging call in the error branch. Retry `EINTR` on blocking calls, but do not retry `close`. `memcmp` on a secret leaks timing.
- Banned functions (`strcpy`, `sprintf`, `gets`) are a finding only with a flow from attacker data to the call; a constant-sized internal source is a hardening note. Do not clear a candidate because the upstream project fixed it in some version: cite the line in this tree that holds the guard, or it is not there.
- Bugs the memory-safety list does not name: a separator character accepted inside a value and re-emitted, a shared helper that enforces a rule at some call sites and not others, and a state machine that accepts a message in the wrong state. These need a read of what a value is allowed to be.

## 3. Rust and PyO3

- `unwrap()`, `expect()`, indexing or `as` casts reachable from Python input; a panic crossing the boundary.
- `unsafe` without `// SAFETY:`; an `unsafe fn` without `# Safety`; `unsafe impl Send` or `transmute` to quiet the compiler; a safe function that can cause undefined behaviour through safe calls.
- A Python object kept past the call without `Py<T>`; GIL released while touching Python objects; a lock guard held across a call back into Python.
- Errors mapped to the wrong exception or with the cause dropped.
- `#[pymodule(gil_used = false)]` claimed with shared mutable state.
- Slices built with `from_raw_parts` or `get_unchecked` from lengths that came from Python; arithmetic on lengths and offsets that wraps in release builds (`checked_add`, `try_from`).
- A safe `pub fn` must be sound for every input safe code can give it: a `/// # Safety` note on a safe function documents a caller duty it does not enforce, which is itself the bug; only an `unsafe fn` may shift the duty to the caller. The same goes for `unsafe impl Send`/`Sync`: a comment does not make `struct W(*mut Handle)` thread-safe, an enforced invariant does.
- `debug_assert!` as the only guard of an `unsafe` operation (compiled out of release); `*ptr = value` over memory that was never initialised (drops garbage; use `ptr::write`); `ptr::read` of an owning type without `forget`/`ManuallyDrop` (two owners); `Vec::set_len` past initialised slots; `get_unchecked` bounded by capacity instead of length; a trait method's return value (`Read::read`, `ExactSizeIterator::len`) trusted as a size in `unsafe`.
- Transmutes and casts: an integer to an enum or `bool` without a check; a fat pointer (`&dyn Trait`, `&[T]`) turned thin or passed through `extern "C"`; `usize as *mut T` with no exposed provenance; references into `#[repr(packed)]` fields (`println!("{}", s.field)` borrows it).
- A closure or callback registered with C: a panic in it aborts the process (checked: a panic inside an `extern "C" fn` printed "non-unwinding panic. aborting."), so it needs `catch_unwind` and an error code; `CString::new(..)?.as_ptr()` kept past the statement dangles; memory from a C allocator freed through Rust's (`Box::from_raw`) or the reverse; a raw fd wrapped twice or leaked.
- Denial of service from Python input: `with_capacity(n)` or a loop bound taken from a field; a recursive type parsed, printed or dropped at attacker-chosen depth (a stack overflow aborts the whole process and `catch_unwind` cannot stop it; the default `Drop` of a long `Box` chain recurses); `&s[a..b]` at a non-character boundary panics even when in bounds (`s.get(a..b)` returns `None`, checked); `/` or `%` by zero panics in every profile, including through `wrapping_div`; `f64 as usize` saturates silently (`NaN` becomes 0, infinity `usize::MAX`, checked).
- Paths: `Path::join` with an absolute argument returns the argument (`join("/etc/passwd")` is `/etc/passwd`, checked), and `..` stays; check before the call, since `canonicalize` fails on a path that does not exist yet.
- Secrets (keys, tokens) held in native memory: cleared on drop (`zeroize`), not copied into logs or panic messages, compared in constant time (`subtle`) rather than with `==`. A key type should not derive `Copy` (every copy is a silent duplicate that never drops), `Clone`, `Debug` or `Serialize` without a reason; `mem::forget`, `ManuallyDrop`, `Box::leak` and `Box::into_raw` skip the `Drop` that wipes; a `static` is never dropped; a secret held across an `.await` lives in the future's state, which is freed unwiped if the future is cancelled; `ptr::write_bytes` as a wipe can be removed as a dead store (use `zeroize`). The same applies in C: `memset` before `free` can be deleted by the optimiser.

## 4. C++ bindings (nanobind, pybind11)

- A returned pointer or reference with no stated return value policy; a raw owning pointer in a signature; a reference kept into an object Python can free or resize.
- An exception that can escape a destructor or a `noexcept` function; an index or size from Python used unchecked.
- Python touched while the GIL is released; a free-threaded opt-in (`FREE_THREADED`, `py::mod_gil_not_used()`) with unsynchronised shared state.

## 5. Layout and ABI

- Struct, enum and integer widths that differ by platform; `#[repr(C)]` missing on a shared struct.
- Exceptions or panics unwinding through an ABI that forbids it; callbacks run after the module is torn down; an API that needs one thread called from another.
- A module that claims `abi3` using a non-limited API symbol; a wheel tag that does not match what was built.

## 6. Tests and tools to ask for

- Sanitizer run (ASan, UBSan, TSan for threads), Miri for Rust `unsafe` (and loom where it shares state between threads), a Python debug build, a 10,000-call leak loop.
- A test for each error path, and for empty, maximum and negative sizes.
- A fuzz target for any parser of untrusted bytes.
- The pure-Python reference compared against the native result.

## Report

Use the confirmed / needs-validation / rejected split from `security-audit/reporting.md`. For each finding: where (`file:line`), the rule broken, the failing input or call, the smallest fix, and the regression test. Say which of the sanitizer, Miri or test runs you did not perform.
