# C++ behind a Python API

Every object that crosses the boundary has two possible owners, and C++ will not tell you when both think they own it, or neither does. Ask of each binding: who frees this, and what else must stay alive while Python holds it? Read [architecture.md](architecture.md) first: the seam, the pure-Python reference and the "go native only on evidence" rule apply unchanged.

Checked against the nanobind documentation (3.2 development branch) and the pybind11 documentation (v3) on 10 November 2026; nothing here was compiled. Check the installed version before relying on an option ([checking-apis.md](../../workflow/checking-apis.md)).

## Which binding library

- New bindings: nanobind. Existing pybind11 code stays pybind11; the two APIs are close, and a port is a task of its own, not a side effect.
- An existing C library with no new C++: `cffi`, not a C++ wrapper.
- Build with scikit-build-core and CMake (`build-backend = "scikit_build_core.build"`); the native module is private (`_core`, `_impl`) and a typed Python package re-exports from it.

## Ownership and lifetime

- State the return value policy on every binding that returns a pointer or reference. The default (`rv_policy::automatic` in nanobind, `return_value_policy::automatic` in pybind11) takes ownership of a returned raw pointer, so returning a pointer to a global or a member makes Python free memory C++ still owns.
- A method that returns a reference into `self`: `reference_internal`, which keeps the parent alive while the child is used. Something Python must keep alive for another reason: `keep_alive`.
- Make transfer visible in the type: `std::unique_ptr<T>` to hand an object over, `std::shared_ptr<T>` (or intrusive counting in nanobind) when both sides share it. A raw owning pointer in a bound signature is a finding.
- Never keep a `T&`, an iterator or a `std::string_view` into something Python can free or resize after the call returns.
- Large arrays cross as buffers, not element by element: `nb::ndarray<...>` in nanobind, `py::array_t` or the buffer protocol in pybind11. State the dtype, shape and contiguity you accept, and reject the rest with a `TypeError`.

## Errors

- Both libraries translate `std::exception` and its standard subclasses at the boundary (`std::invalid_argument` to `ValueError`, `std::out_of_range` to `IndexError`, `std::bad_alloc` to `MemoryError`, anything else derived from `std::exception` to `RuntimeError`). Throw the type whose Python translation the caller expects; register a translator for the package's own root exception.
- An exception thrown from a destructor or a `noexcept` function never reaches the translator: the C++ runtime calls `std::terminate()` and the interpreter dies. Catch inside such functions. A type not derived from `std::exception` arrives as a bare `RuntimeError` with no message, so do not throw one.
- No error codes or sentinel returns to Python. Validate sizes and indexes from Python before using them; an unchecked `operator[]` on input is undefined behaviour, not an `IndexError`.

## GIL and threads

- Release the GIL around long work that touches no Python object: `gil_scoped_release` in the function body, or `nb::call_guard<nb::gil_scoped_release>()` on the binding. Take it back (`gil_scoped_acquire`) before any call into Python, including a callback or a destructor of a held Python object.
- Free-threaded builds are opt-in: `FREE_THREADED` in `nanobind_add_module`, `py::mod_gil_not_used()` in `PYBIND11_MODULE`. Declare it only after the module's shared state is synchronised, and test on a free-threaded interpreter ([ci-wheels.md](ci-wheels.md)).

## Types and stubs

- nanobind generates stubs from its own signature data: `nanobind_add_stub(...)` in CMake or `python -m nanobind.stubgen`. Ship the `.pyi` and `py.typed`, and check them in CI with `python -m mypy.stubtest <pkg>`.
- pybind11 has no built-in generator; write the `.pyi` by hand or generate it and review it, and run the same `stubtest` check.
- No C++ type name in a public Python signature or error message.

## Wheels

- nanobind `STABLE_ABI` builds one wheel per platform for Python 3.12 and newer and is ignored on older versions, so the matrix still needs per-version wheels below 3.12. It costs some speed; measure before choosing it. It is ignored in free-threaded builds.
- Build flags: warnings as errors in CI (`-Wall -Wextra -Werror`), the C++ standard set once in CMake, no `-march=native` in a wheel.

## Testing

- ASan and UBSan build with the full suite; TSan when the GIL is released or free-threading is declared.
- nanobind reports leaked instances, types and functions at interpreter exit. Treat a report as a failing test; do not call `nb::set_leak_warnings(false)` to quiet it.
- The same inputs through the pure-Python reference, compared. Every error path, and empty, maximum and negative sizes.

Mistakes to check before finishing: [smells.md](smells.md). Reviewing someone else's bindings: `review/native-boundary.md`.
