# Debugging

Debugging is testing a hypothesis about a cause, not trying changes until the symptom stops. A symptom that disappears without a stated cause has usually only moved. The loop: reproduce, narrow, name the cause, fix that, prove it with the test that failed first, look for the same bug elsewhere.

## 1. Reproduce

- A failing test, or the smallest failing input, before any edit. A fix starts red ([testing.md](../testing/testing.md)). Cannot reproduce: say so and ask for the input or log; do not fix what you cannot see fail.
- Read the whole traceback, bottom frame first, and the `__cause__` or `__context__` chain above it. The decisive line is usually the last frame in the project's own code, not the library's.
- Flaky: run it in a loop (`for i in $(seq 30); do pytest path::test -x -q || break; done`) to get a failure rate, then look for what differs between runs: order (`-p no:randomly`, run the test alone), time, shared state, network, a seed, a leftover file.

- Make the loop one command: a script or a single `pytest` line that reproduces the failure and prints a pass or fail, so each attempt costs one call. Change one thing between runs.
- Before trusting a result, confirm your edit is the code that runs: print `module.__file__`, and for a doubtful case put a deliberate `raise SystemExit("reached")` on the line you changed and see it fire. A stale install, an editable install pointing elsewhere or a cached `.pyc` explains many "the fix did nothing" reports.

## 2. Narrow

- Cut the input and the code path in half until the failure is the smallest case. A regression with a known good commit: `git bisect run pytest path::test -q`.
- Look at the boundary where good data turns bad: print or `breakpoint()` at the entry and exit of the suspect function, or `pytest --pdb -x`. Prefer a debugger or a print of the real value over reasoning about what it should be.
- Hangs: `python -X faulthandler` and `faulthandler.dump_traceback_later(30)`, or `py-spy dump --pid`. Memory growth: `tracemalloc` snapshots before and after. Slow imports: `python -X importtime`. Hidden warnings: `python -X dev -W error`.
| Symptom | First tool |
| --- | --- |
| Wrong value somewhere in the middle | `breakpoint()` or `pytest --pdb -x` at the boundary; print the real value |
| Hangs, never finishes | `py-spy dump --pid`, `faulthandler.dump_traceback_later` |
| Regression, last good commit known | `git bisect run <command>` |
| Slow | a sampling profiler (`py-spy record`), then [performance](../performance/index.md) |
| Memory grows | `tracemalloc` snapshots, `memray` |
| Only fails in CI | the same Python, locked dependencies and environment variables as CI; compare `pip freeze` output |
| Native crash or segfault | `python -X faulthandler`, a debug build, the sanitizer jobs in [ci-wheels.md](../library/native/ci-wheels.md) |

- "Works on my machine": check the interpreter and the package that actually loaded (`python -c "import x; print(x.__file__, x.__version__)"`), the environment the project's runner uses, a stale install or `.pyc`, and the Python target.

## 3. Name the cause

- One sentence, with the evidence: "`totals_per_customer` runs one query per customer, so 40k customers is 40k round trips". If you cannot write it, you are still investigating.
- Test one hypothesis at a time, and say beforehand what you expect to see if it is right. A change that "fixes" it without a reason is a second bug.
- After two or three failed attempts, stop guessing: re-read from the symptom, list what you assumed without checking, and check the cheapest assumption first. Still stuck after a fourth: report what you know, what you ruled out and what to try, and ask.

## 4. Fix and prove

- Fix the cause, not the place the error surfaced. A `try/except` around the failing line, a default for the missing value, a retry or a longer timeout is a patch over a symptom unless you can say why that is the right behaviour.
- Never special-case inputs or hardcode expected outputs. No sleeps, retries or longer timeouts until the cause of a race is known; make it deterministic instead (inject the clock, seed the randomness, wait on the event). Do not pin, downgrade or swap a dependency, or edit `sys.path`, to get past an error without explaining why.
- Do not silence the tool that found it: no `# type: ignore`, `# noqa`, `cast()`, `Any`, and no loosened linter, type-checker or pytest config. If an ignore is truly needed, name the code (`# type: ignore[arg-type]`) and say why in a comment.
- The test that failed first now passes, the neighbouring tests still pass, and you `git grep` for the same pattern elsewhere; report other hits instead of silently widening the diff.
- Report: the cause in one sentence, how you showed it, the test, and anything you could not verify.
