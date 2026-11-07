# After the profile: fixes in order of leverage

Use this once a profile has named the hot spot. Ratios were measured on one machine (Python 3.13.18, 7 November 2026) with `timeit` and `tracemalloc`; expect the same order of magnitude, not the same number, and re-measure on the real input.

## Contents

- Data structure and algorithm
- Do less work
- Memory
- Strings
- Concurrency last

## Data structure and algorithm

- Membership tests in a loop: build a `set` (or `dict`) once. `x in list` over 5,000 items against `x in set`: about 500 times faster.
- A queue: `collections.deque` with `popleft()` instead of `list.pop(0)`. At 100,000 items: about 200 times faster.
- Repeated lookups of the same key, nested loops over two collections, a sort inside a loop: index once, loop once, sort once.
- A query or request inside a loop (N+1): batch it. The application bundle covers the ORM forms, if installed.

## Do less work

- Cache a pure function with `functools.cache` or `lru_cache(maxsize=n)`. Arguments must be hashable; `cache` has no bound, so a long-running process with many distinct arguments grows without limit.
- `lru_cache` on a method keeps `self` alive: the instance was not collected after `del` in the check below. Cache a module-level function keyed by value, or use `cached_property` for a per-instance value.

```python
import gc
import weakref
from functools import lru_cache


class Service:
    @lru_cache(maxsize=None)
    def value(self, x):
        return x


service = Service()
service.value(1)
ref = weakref.ref(service)
del service
gc.collect()
assert ref() is not None  # the cache still holds the instance
```

## Memory

- A pipeline that only iterates: a generator expression instead of a list. `sum` over 1,000,000 doubled integers peaked at about 40 MB as a list and effectively nothing as a generator.
- Many small objects with fixed fields: `__slots__` (or `@dataclass(slots=True)`). 100,000 two-field instances: 9.6 MB plain, 5.6 MB with slots, about 1.7 times smaller.
- Large numeric data: `array.array` or NumPy, not a list of Python numbers.

## Strings

- Build with `"".join(parts)`. `s += x` in a loop was about 1.8 times slower at 200,000 appends here; CPython sometimes extends a string in place when it has one reference, so the loop form is not always quadratic, and the result differs between implementations.

## Concurrency last

- Waiting on I/O: threads or `asyncio`. CPU-bound Python: processes (`ProcessPoolExecutor`), mind the pickling cost of arguments and results. Free-threaded builds (PEP 703, PEP 779) can run threads in parallel but were not tested here.
- Measure the whole task before and after; keep a change only if the profile and the timing both show the gain.
