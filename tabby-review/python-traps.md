# Python traps worth probing

Each was run on Python 3.13 except the ones marked (documented), which are documented behaviour that was not run here. Use them as probes ([bug-hunt.md](bug-hunt.md)): write the input, run it, report what happened.

- `round(2.5)` is 2 (banker's rounding); `-7 // 2` is -4 and `-7 % 2` is 1; `is` is not `==`; float equality.
- `os.environ` values are strings, so `"0"` is truthy; `argparse` `type=bool` turns `"False"` into `True`; JSON turns integer keys into strings and `json.dumps(float("nan"))` writes `NaN`, which is not valid JSON.
- `datetime.utcnow()` is naive and deprecated since 3.12; `sorted([1, "a"])` raises; a class with `__eq__` and no `__hash__` is unhashable.
- A closure built in a loop sees the last value (`[f() for f in [lambda: i for i in range(3)]]` is `[2, 2, 2]`; `lambda i=i: i` fixes it). A project file named `random.py` or `email.py` shadows the standard module.
- `asyncio.gather` without `return_exceptions=True` raises the first error and leaves the other tasks running (checked); a blocking call inside `async def` stalls every task (documented); a task nothing references can be garbage-collected (documented).
- sqlite3's `with conn:` commits but leaves the connection open (checked). `open` without `encoding` and HTTP calls with no timeout (documented); `lru_cache` on a method keeps `self` alive.
- `except Exception` with a default return hides the real failure; `assert` is removed under `python -O`.
- A mutable class attribute (`permissions = []` on a class) is shared by every instance: `u1.permissions.append("admin")` makes `u2` an admin too (documented). A loop variable outlives the loop (`print(item)` after `for item in items`).
- `"{0.cfg.secret}".format(obj)` follows attributes, and through a function it reaches module globals (`{0.__init__.__globals__[__name__]}`): never use a user-supplied string as a `str.format` template (checked). `getattr(obj, name)` with a request-supplied `name` reaches `__class__` and `__dict__` (checked).
- `json.loads('{"admin": false, "admin": true}')` keeps the last duplicate key (checked), so two parsers that disagree on duplicates can be played against each other; Python's JSON keys are case-sensitive (checked). Plain dict parsing ignores unknown fields; use a model that forbids them.
- `re.match(r"^admin$", "admin\n")` matches because `$` also matches before a trailing newline; `re.fullmatch` and `\Z` do not (checked). `"İ".lower()` is two code points and `"STRASSE".lower() == "straße".lower()` is false while `casefold()` makes them equal (checked): compare identifiers exactly, or with `casefold()`. `len("👨‍👩‍👧‍👦")` is 7: slicing user text by code points can split a character (checked).
- `Decimal(0.1)` carries the binary float (`0.1000000000000000055511151231257827…`); write `Decimal("0.1")` (checked). Calling a coroutine without `await` runs nothing and only emits `RuntimeWarning: coroutine ... was never awaited` (checked).
- `asyncio.CancelledError` is not an `Exception`, so `except Exception` lets cancellation through, while `except BaseException` or a bare `except` that does not re-raise swallows it and the task never ends as cancelled (checked).
- `a, b, c = some_iterable` stops after one extra element and raises `ValueError`: a prebuilt list failed in microseconds and an endless generator was consumed only 4 items (checked), so unpacking is not a way to exhaust memory. An exception raised inside an `except` block keeps the original as `__context__` (checked).
- `n += 1` on a shared counter is several bytecodes and needs a lock; 8 threads × 300,000 increments on 3.13 with the GIL gave the exact total, so it did not reproduce there (documented as unsafe, and likely to lose updates on free-threaded builds).
- Ignoring the result of `close()` or `flush()` on a file opened for writing hides a failed write.
