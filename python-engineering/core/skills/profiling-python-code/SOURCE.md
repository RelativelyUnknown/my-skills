# Source

`references/after-the-profile.md` is adapted from one upstream skill. The rest of this skill is original to this repository.

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-performance-optimization/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream licence is kept as `LICENSE.wshobson` and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (100 lines) and details (759 lines) are a profiler tutorial (cProfile, line_profiler, memory_profiler, py-spy) plus an optimization catalogue. This skill's tool table already covers profilers more completely (Tachyon, py-spy, scalene, pyinstrument, memray, tracemalloc, pyperf), so the tutorial is not copied.
- Folded in, rewritten around a measure-first order: the fixes to try once a profile names a hot spot (data structure, doing less work, memory, strings, concurrency). Every ratio in the reference was measured in the container (Python 3.13.18) with `timeit` and `tracemalloc`: set against list membership about 500 times, `deque.popleft` against `list.pop(0)` about 200 times, a list against a generator about 40 MB against none, `__slots__` about 1.7 times smaller, `join` against `+=` about 1.8 times. The `lru_cache`-on-a-method instance leak was run; the example block passes.
- Not run: free-threaded builds (PEP 703, PEP 779) and multiprocessing costs, mentioned as pointers only.
