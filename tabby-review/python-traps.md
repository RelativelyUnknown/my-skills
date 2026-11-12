# Python traps worth probing

Each was run on Python 3.13 except the ones marked (documented), which are documented behaviour that was not run here. Use them as probes ([bug-hunt.md](bug-hunt.md)): write the input, run it, report what happened.

- `round(2.5)` is 2 (banker's rounding); `-7 // 2` is -4 and `-7 % 2` is 1; `is` is not `==`; float equality.
- `os.environ` values are strings, so `"0"` is truthy; `argparse` `type=bool` turns `"False"` into `True`; JSON turns integer keys into strings and `json.dumps(float("nan"))` writes `NaN`, which is not valid JSON.
- `datetime.utcnow()` is naive and deprecated since 3.12; `sorted([1, "a"])` raises; a class with `__eq__` and no `__hash__` is unhashable.
- A closure built in a loop sees the last value (`[f() for f in [lambda: i for i in range(3)]]` is `[2, 2, 2]`; `lambda i=i: i` fixes it). A project file named `random.py` or `email.py` shadows the standard module.
- `asyncio.gather` without `return_exceptions=True` raises the first error and leaves the other tasks running (checked); a blocking call inside `async def` stalls every task (documented); a task nothing references can be garbage-collected (documented).
- sqlite3's `with conn:` commits but leaves the connection open (checked). `open` without `encoding` and HTTP calls with no timeout (documented); `lru_cache` on a method keeps `self` alive.
- `except Exception` with a default return hides the real failure; `assert` is removed under `python -O`.

