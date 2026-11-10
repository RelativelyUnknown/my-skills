# Performance

Optimizing without a profile is guessing. Find the one place that dominates, fix it, prove it with numbers, stop.

## Measure first

- Use realistic input: production-sized data or a representative sample, not a toy case.
- Write the measured command down, run it at least five times, record the median and spread, and note the machine and Python version. A change inside the run-to-run spread is no change. Turn off what distorts timing (coverage, debuggers, verbose logging).
- Use profilers already in the dev group; `uvx <tool>` runs one without adding it to the project. Propose adding one in the report instead of installing it silently.
- Prefer a sampling profiler (stdlib `profiling.sampling` on 3.15, else `py-spy`): low overhead, realistic proportions. `cProfile` for exact call counts, `line_profiler` for lines inside one known function, `memray` or `tracemalloc` for memory, `pyinstrument` for a readable call tree of async handlers.
- Read the flame graph for the widest frames owned by project code. A library frame under your call usually means "called too often" or "with too much data", not "the library is slow".
- For small functions use `pyperf` or `timeit`, never a single `time.time()` difference.

## Fix in order of leverage

1. **Do less work.** A `set` or `dict` built once for membership tests (500 times faster than `x in list` over 5,000 items), `collections.deque` with `popleft()` instead of `list.pop(0)`, index once and loop once, one query instead of N, built-ins or NumPy instead of manual loops.
2. **Cache a pure function** with `functools.cache` or `lru_cache(maxsize=n)`. Arguments must be hashable; `cache` has no bound. `lru_cache` on a method keeps `self` alive: cache a module-level function keyed by value, or use `cached_property`.
3. **Memory.** A generator expression instead of a list when you only iterate; `__slots__` or `@dataclass(slots=True)` for many small objects; `array.array` or NumPy for large numeric data.
4. **Strings.** `"".join(parts)`, not `s += x` in a loop.
5. **A different library or a native extension** only when a profile shows the work cannot be reduced: the ladder in [reuse.md](../code/reuse.md) (the standard library, then the community's standard library), then a niche package that earns its place ([dependencies.md](../dependencies/dependencies.md)), then native code ([native architecture](../library/native/architecture.md)).
6. **Concurrency last.** Waiting on I/O: threads or `asyncio`. CPU-bound Python: `ProcessPoolExecutor` (mind the pickling cost), or the free-threaded build when every dependency supports it.
7. **Micro-optimizations** only on lines the profile names, and only when the gain is measurable.

Ratios above were measured on one machine; expect the same order of magnitude, not the same number, and re-measure on the real input. Never trade correctness for speed: run the full test suite after each change, and keep a win that matters guarded by a benchmark test only when the project already runs benchmarks.

## Report

The command measured, the baseline and result (median and spread), the profile evidence that pointed at the change, what changed, and hot spots seen but left alone.
