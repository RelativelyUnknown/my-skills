---
name: profiling-python-code
description: "Finds where Python code spends time or memory before optimizing: sampling and tracing profilers, memory profilers, reliable benchmarks, before/after numbers. Use when code is slow, uses too much memory, a speedup is requested, or before swapping in a faster library."
argument-hint: "[python=3.12 runner=uv report=normal]"
---

# Profiling Python code

Optimizing without a profile is guessing. Find the one place that dominates, fix it, prove it with numbers, stop.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`python.target`, `runner`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Use profilers already in the dev group; propose adding one in the report rather than installing it silently. `uvx <tool>` runs a profiler without adding it to the project.

Spark and Databricks jobs: profile the query plan instead (`tuning-spark-jobs`).

## 1. Reproduce and baseline

- Use realistic input: production-sized data or a representative sample, not a toy case where everything is fast.
- Write the measured command down, run it at least five times, and record the median and spread. Note the machine, Python version and whether caches are warm.
- Turn off what distorts timing: coverage, debuggers, `PYTHONDEVMODE`, verbose logging.

## 2. Find the hot spot

| Question | Tool | Command |
| --- | --- | --- |
| Where does wall time go? (default) | Sampling profiler: stdlib Tachyon on 3.15, else py-spy | `python -m profiling.sampling run --flamegraph -o profile.html script.py`; `py-spy record -o profile.svg -- python script.py` |
| What is a running process doing right now? | Attach by PID | `python -m profiling.sampling attach -d 30 <pid>`; `py-spy dump --pid <pid>` |
| Python time vs native time vs memory, together | scalene | `scalene script.py` |
| Readable call tree, including async web handlers | pyinstrument | `pyinstrument script.py`, or its ASGI/WSGI middleware |
| Exact call counts | Tracing profiler: `cProfile` (alias of `profiling.tracing` on 3.15) | `python -m cProfile -o out.prof script.py`, then `python -m pstats out.prof` or `snakeviz out.prof` |
| Which lines inside one known function | line_profiler | `kernprof -lv script.py` with `@profile` on that function |
| Who allocates memory, and does it leak? | memray (Linux, macOS), stdlib `tracemalloc` | `memray run -o run.bin script.py && memray flamegraph run.bin` |

- Prefer sampling profilers: low overhead, safe on production processes, realistic proportions. Tracing profilers inflate code with many small calls.
- Attaching to a process needs ptrace rights (Linux: root, `CAP_SYS_PTRACE` or `ptrace_scope=0`; macOS: root). The stdlib sampler must run on the same Python minor version and build (free-threaded or standard) as the target. Say so instead of escalating privileges yourself.
- Profile threads and asyncio explicitly when they matter (`--all-threads`, `--async-aware`; `py-spy --threads`, `--idle`).
- Read the flame graph for the widest frames owned by project code. Library frames under your call usually mean "called too often" or "called with too much data", not "the library is slow".

## 3. Fix in this order

1. **Do less work**: a better algorithm or data structure (a `set` for membership, a dict index instead of a nested loop), no repeated work (hoist out of loops, `functools.cache` for pure repeated calls).
2. **Batch I/O**: one query instead of N, bulk inserts, a shared HTTP client, concurrency for I/O waits (`asyncio.TaskGroup`, `ThreadPoolExecutor`).
3. **Move loops out of Python**: NumPy, Polars or DuckDB operations, built-ins (`sum`, `sorted`, `str.join`), comprehensions over manual appends.
4. **A faster library** for the measured hot path: `writing-python-code` (`references/faster-libraries.md`).
5. **Parallelism** for CPU-bound work: `ProcessPoolExecutor`, or the free-threaded build when every dependency supports it.
6. **Micro-optimizations** last, only on lines the profile names, and only when the gain is measurable.

Never trade correctness for speed: run the full test suite after each change. Keep readable code unless the profile says the line matters.

## 4. Prove it

- Rerun the same command the same way and compare medians. A change within the run-to-run spread is no change.
- For small functions, use `pyperf` (`python -m pyperf timeit ...`; `python -m pyperf system tune` reduces noise) or `timeit`, never a single `time.time()` difference.
- Guard a win that matters with a benchmark test (`pytest-benchmark`, or `pytest-memray` with a memory limit) only when the project already runs benchmarks or asks for one.

## Report

Follow `writing-python-code` for the report, and include: the command measured, the baseline and result (median and spread), the profile evidence that pointed at the change, what was changed, and hot spots seen but left alone.
