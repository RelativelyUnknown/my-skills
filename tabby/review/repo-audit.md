# Auditing a whole repository

Find what will hurt whoever owns this next: wrong, unsafe, breaking under load, untested where it matters, slow, or not needed. Report only what you can show with a concrete case. This is a report; change nothing unless asked. For security alone, use [security-audit/process.md](security-audit/process.md).

## Map first

- Read the README, the deploy and build config, the dependency list, the entry points (CLI, routes, jobs, handlers) and the tests. Find the heavily changed files: `git log --since=6.months --name-only --pretty=format: | sort | uniq -c | sort -rn | head`.
- Find the expected load from `users:` and `growth:` in `## Tabby`, or the README: one person running a script, or many users and processes at once. Say which you assumed.
- Trace the main flows end to end: where data comes in, what is stored, what goes out. Read money, authentication, data writes and background jobs completely. In a big repository go deep where a mistake costs most, and say what you did not read.

## Look for, in this order

1. **Bug:** a wrong result, a crash, a missed edge (empty, zero, last item, rounding, time zones), two places applying the same rule differently.
2. **Risk:** unsafe handling of input, secrets in code, data loss (swallowed errors, writes in the wrong order, no transaction). Pass these to the security audit if they need tracing.
3. **Load:** fine for one user, wrong for many: check-then-write races, a query per item, a list or cache that only grows, per-process state that must be shared, quadratic work on caller-sized input.
4. **Missing test:** risky logic (a branch, a parser, money, a data write) with no test that would fail if it broke. One good test, not coverage.
5. **Speed:** only large slowdowns are findings; small ones are suggestions.
6. **Lean:** code that can go: unused code, options and flags nobody sets, a second helper doing the same job, a dependency doing what the standard library does, an abstraction with one implementation.

## Before you report

- Every finding has the input or situation where it goes wrong. No case, no finding.
- Before calling code dead, find why it exists: callers including entry points in `pyproject.toml`, framework registration, config and `getattr` use, and `git log -S<name>`. Something reachable only from outside the repository is not dead.
- A `# shortcut:` comment that names its limit and a trigger is a decision, not a finding, unless the expected load already crosses the limit. List the markers with `git grep -nE "# ?shortcut:"` and tag any with no trigger.

## Output

Numbered findings, most serious first, so the owner can answer "fix 2 and 5". For each: `file:line`, what is wrong, when it fails, the smallest fix, and what skipping it costs. Then: the load you assumed, `Not read:` (what you skipped), and a verdict. A repository with no findings gets the verdict and what you checked.
