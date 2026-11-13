# Debugging

Debugging is testing a hypothesis about a cause, not trying changes until the symptom stops. A symptom that disappears without a stated cause has usually only moved. The loop: reproduce, narrow, name the cause, fix that, prove it with the test that failed first, look for the same bug elsewhere.

## 1. Reproduce

- A failing test, or the smallest failing input, before any edit. A fix starts red ([testing.md](../testing/testing.md)). Cannot reproduce: say so and ask for the input or log; do not fix what you cannot see fail.
- Read the whole traceback, bottom frame first, and the `__cause__` or `__context__` chain above it. The decisive line is usually the last frame in the project's own code, not the library's.
- Flaky: run it in a loop (`for i in $(seq 30); do pytest path::test -x -q || break; done`) to get a failure rate, then look for what differs between runs: order (`-p no:randomly`, run the test alone), time, shared state, network, a seed, a leftover file.
- Make the loop one command: a script or a single `pytest` line that reproduces the failure and prints pass or fail, with setup and the run together (`rm -r data && ./launch.sh`) and variables set inline (`FLAG=on python x.py`, not an earlier `export`), so a stale step cannot make a hypothesis look tested. Change one thing between runs. Make it fast (a tiny input, one process, no network): a 2-second loop gets run hundreds of times and a 10-minute one gets abandoned. In a notebook or REPL, rerun from a clean start before believing a result.
- Before trusting a result, confirm your edit is the code that runs: print `module.__file__`, and for a doubtful case put a deliberate `raise SystemExit("reached")` on the line you changed and see it fire. A stale install, an editable install pointing elsewhere or a cached `.pyc` explains many "the fix did nothing" reports.

## 2. Narrow

- Cut the input and the code path in half until the failure is the smallest case. A regression with a known good commit: `git bisect run pytest path::test -q`; 1,024 commits take ten steps. A commit that cannot be tested (a different bug in the range, an API change) is `git bisect skip`; to find the commit that *fixed* something, name the states so they cannot be confused: `git bisect start --term-old=broken --term-new=fixed`. Dependencies may differ across the range, so reinstall the right ones before trusting a verdict.
- A debugger, a `print`, a forced-synchronous flag or `PYTHONASYNCIODEBUG` changes timing, so a race or deadlock can vanish when observed. For those use a tracer that does not stop the process (`py-spy dump --pid`, `strace -f -p PID`, logging with thread ids) and note which tool made the failure disappear; that is evidence about the cause.
- To debug a failure that already happened, run under the debugger and let the exception stop it: `python -m pdb -c continue prog.py` ends in a post-mortem prompt at the failing frame (checked). `pytest --pdb` does the same for a test.

| Symptom | First tool |
| --- | --- |
| Wrong value somewhere in the middle | `breakpoint()` or `pytest --pdb -x` where good data turns bad; look at the real value rather than reasoning about what it should be |
| Hangs, never finishes | `py-spy dump --pid`, `python -X faulthandler`, `faulthandler.dump_traceback_later(30)` |
| Regression, last good commit known | `git bisect run <command>` |
| Slow | a sampling profiler (`py-spy record`), then [performance](../performance/index.md); judge a change with one measuring method used the same way, because `cProfile`, `line_profiler` and `timeit` disagree on absolute numbers |
| Memory grows | `tracemalloc` snapshots before and after, `memray` |
| Only fails in CI, or "works on my machine" | the same Python, locked dependencies and environment as CI; compare `pip freeze`; check which interpreter and package actually loaded (`python -c "import x; print(x.__file__, x.__version__)"`), a stale install or `.pyc` |
| Slow imports, hidden warnings | `python -X importtime`; `python -X dev -W error` |
| Native crash or segfault | `python -X faulthandler`, a debug build, the sanitizer jobs in [ci-wheels.md](../library/native/ci-wheels.md) |


## 3. Name the cause

- One sentence, with the evidence: "`totals_per_customer` runs one query per customer, so 40k customers is 40k round trips". If you cannot write it, you are still investigating.
- Test one hypothesis at a time, and say beforehand what you expect to see if it is right. A change that "fixes" it without a reason is a second bug.
- After two or three failed attempts, stop guessing: re-read from the symptom, list what you assumed without checking, and check the cheapest assumption first. Still stuck after a fourth: report what you know, what you ruled out and what to try, and ask.

## 4. Fix and prove

- Fix the cause, not the place the error surfaced. A `try/except` around the failing line, a default for the missing value, a retry or a longer timeout is a patch over a symptom unless you can say why that is the right behaviour.
- The core rules apply: no special-casing, no sleeps, retries or longer timeouts before the cause of a race is known (make it deterministic: inject the clock, seed the randomness, wait on the event), no pinning or swapping a dependency to get past an error without saying why, and no silencing the tool that found it (name the code in an unavoidable `# type: ignore[arg-type]` and say why).
- Fix the broken invariant, not the one line: ask what must always be true here, then `git grep` inside that boundary for every other instance of the same mistake and fix or report them. The smallest fix is the smallest *reviewable invariant-level* change, not the fewest lines.
- The test that failed first now passes, and the whole suite gives the same results as before your change apart from that test (run it before and after and compare). Then revert your fix once and watch the test fail again; if it does not, the test is not testing the fix.
- Report: the cause in one sentence, how you showed it, the test, and anything you could not verify.
