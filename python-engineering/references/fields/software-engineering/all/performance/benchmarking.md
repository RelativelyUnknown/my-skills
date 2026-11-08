# Benchmarking

- Rerun the same command the same way and compare medians. A change within the run-to-run spread is no change.
- For small functions, use `pyperf` (`python -m pyperf timeit ...`; `python -m pyperf system tune` reduces noise) or `timeit`, never a single `time.time()` difference.
- Guard a win that matters with a benchmark test (`pytest-benchmark`, or `pytest-memray` with a memory limit) only when the project already runs benchmarks or asks for one.

Once the profile names a hot spot, try the fixes in order of leverage: [hot-path-fixes.md](hot-path-fixes.md).

Report the command measured, the baseline and result (median and spread), the profile evidence that pointed at the change, what was changed, and hot spots seen but left alone.
