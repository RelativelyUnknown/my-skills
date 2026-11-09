# Resources

A resource has one owner, and the owner releases it on every path: return, exception, cancellation.

- Anything with a close goes in `with` / `async with`: files, sockets, locks, connections, cursors, temp dirs, subprocesses, transactions, HTTP responses. Use `try`/`finally` only for one-off cleanup that has no context manager.
- Acquire in `__enter__` or a factory, not in `__init__`: a constructor does no I/O. Give the class an idempotent `close()` and let `__exit__` call it.
- A `@contextmanager` function puts `yield` inside `try`/`finally`. Without `finally`, an exception in the `with` body skips the cleanup.
- `__exit__` returns `None`. Return `True` only to swallow one named exception you document (`BrokenPipeError` from a client that left), never `Exception` or `BaseException`.
- Several resources, or a number known at run time: `ExitStack` / `AsyncExitStack` with `enter_context` (`callback` for a plain cleanup function). To hand the resources to the caller once acquisition succeeded, `return stack.pop_all()`: if a later step fails, everything opened so far closes; otherwise the caller closes the returned stack.
- Async: cleanup that awaits (rollback, close) still runs after `CancelledError`. Catch `BaseException`, clean up, then `raise`; never catch it and carry on.
- A generator that holds a resource releases it only when it finishes, is closed or is garbage collected. Wrap it in `contextlib.closing(...)`, or consume it inside the `with` that owns the resource.
- Do not rely on `__del__` or reference counting to close things: CPython closes an unreferenced file at once, other implementations later, and a stored traceback keeps it alive.
- Pools and clients live as long as the application (lifespan or a context manager) and are borrowed per task. One connection or session per concurrent task.
- `subprocess.run(..., timeout=, check=True)` kills the child on timeout. `Popen.communicate(timeout=)` does not: catch `TimeoutExpired`, `kill()`, then `communicate()` again, or use `with Popen(...)`.
- Temp files: `tempfile.TemporaryDirectory()` and `NamedTemporaryFile` inside `with`. Python 3.12+ adds `TemporaryDirectory(delete=False)` and `NamedTemporaryFile(delete_on_close=False)`. Replace a file atomically: write a temp file in the same directory, then `os.replace`.
- Streams: collect chunks in a list and `"".join` once; `s += chunk` in a loop can be quadratic. Close the upstream response in `finally` so a consumer that stops early still releases it. Yield chunks as they arrive and time the first one with `time.perf_counter()`.
- Test the error path: a fake resource with a `closed` flag, an exception in the body (`pytest.raises`), then assert the flag. Run the suite with `-W error::ResourceWarning` (or `python -X dev`); unclosed files and sockets are silent otherwise.

Do not write a class where `@contextmanager` fits, and do not wrap `open()` in another manager. Worked examples: [resource-patterns.md](resource-patterns.md).
