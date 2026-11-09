# Profiling

Optimizing without a profile is guessing. Find the one place that dominates, fix it, prove it with numbers, stop.

Use profilers already in the dev group; propose adding one in the report rather than installing it silently. `uvx <tool>` runs a profiler without adding it to the project.

## Reproduce and baseline

- Use realistic input: production-sized data or a representative sample, not a toy case where everything is fast.
- Write the measured command down, run it at least five times, and record the median and spread. Note the machine, Python version and whether caches are warm.
- Turn off what distorts timing: coverage, debuggers, `PYTHONDEVMODE`, verbose logging.

## Find the hot spot

- Where does wall time go? (default) → Sampling profiler: stdlib Tachyon on 3.15, else py-spy: `python -m profiling.sampling run --flamegraph -o profile.html script.py`; `py-spy record -o profile.svg -- python script.py`
- What is a running process doing right now? → Attach by PID: `python -m profiling.sampling attach -d 30 <pid>`; `py-spy dump --pid <pid>`
- Python time vs native time vs memory, together → scalene: `scalene script.py`
- Readable call tree, including async web handlers → pyinstrument: `pyinstrument script.py`, or its ASGI/WSGI middleware
- Exact call counts → Tracing profiler: `cProfile` (alias of `profiling.tracing` on 3.15): `python -m cProfile -o out.prof script.py`, then `python -m pstats out.prof` or `snakeviz out.prof`
- Which lines inside one known function → line_profiler: `kernprof -lv script.py` with `@profile` on that function
- Who allocates memory, and does it leak? → memray (Linux, macOS), stdlib `tracemalloc`: `memray run -o run.bin script.py && memray flamegraph run.bin`

- Prefer sampling profilers: low overhead, safe on production processes, realistic proportions. Tracing profilers inflate code with many small calls.
- Attaching to a process needs ptrace rights (Linux: root, `CAP_SYS_PTRACE` or `ptrace_scope=0`; macOS: root). The stdlib sampler must run on the same Python minor version and build (free-threaded or standard) as the target. Say so instead of escalating privileges yourself.
- Profile threads and asyncio explicitly when they matter (`--all-threads`, `--async-aware`; `py-spy --threads`, `--idle`).
- Read the flame graph for the widest frames owned by project code. Library frames under your call usually mean "called too often" or "called with too much data", not "the library is slow".
