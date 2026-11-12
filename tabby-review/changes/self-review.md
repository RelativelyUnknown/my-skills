# Self-review and diff review

Paths starting `development/` are in the `tabby` skill folder, `../tabby/` from this skill's folder.

Find what is wrong with the diff, and say nothing else. A clean diff gets a short "no findings", not a list of maybes. Prefer a fresh session that did not write the code; a person still reviews multi-file changes.

## Start

1. Read the whole diff (`git diff <base>...<head>`), then the full changed files and the callers of any changed signature.
2. List added suppressions: `git diff <base>...<head> -U0 -- '*.py' | grep -nE '^\+[^+].*(pytest\.mark\.(skip|xfail)|type: ignore|noqa|except Exception|except:)'`. Each hit needs a stated reason or is a finding.
3. Run the project's check command only in a way that writes nothing into the work tree (for example `pytest -p no:cacheprovider`) and does not modify files. Do not modify the code under review.

Learn the project's own rules before judging: `CLAUDE.md`, `AGENTS.md`, the README and the recent commit messages name invariants and past bugs ("this was the bug, keep it"). A diff that violates a documented invariant is a finding even when it compiles and the tests pass; cite the rule. Do not invent generic ones.

Distrust the tests and the comments. A passing suite proves the tested paths, so look for assertions that would still pass if the code were wrong, tests weakened to make the diff green, and paths with no test. Review what the code does, not what a comment or commit message says it does ("killed on exit": check that the kill fires).

Read the commit messages and the pull request text too: they say what the author meant, and a change that does something else is the lead. Compare against the merge base, not the tip of the target branch.

## What to look for, in this order

1. **Correctness** (probes to run: [bug-hunt.md](../bug-hunt.md)). A variable unassigned on a path (a `try` that can fail before the assignment), swallowed errors, wrong boundary, a mutable default, a result that differs from the docstring. Reproduce it when you can and quote the failing input.
   A new module, parser or importer with no test history is its own pass: malformed, huge, empty and Unicode input, a re-run that duplicates rows, a half-written result after an error, offsets computed on one buffer and applied to another. A boundary change is another: a signature or return shape changed on one side only, a new route or command not registered, a missing permission, a migration without matching code, docs claiming behaviour the code lacks.
2. **Regression.** A regression is a new defect the change introduced in behaviour that was supported before and is reachable now (including rejecting invalid input). For each behaviour the diff touches, run the same input through a real entry point (the CLI, the route, the public function) on the old code (export it with `git archive <base> | tar -x -C "$(mktemp -d)"`, which leaves the repository untouched) and on the new, and compare. A helper that fails on an input no caller can produce is not a regression, and "passed before, fails now" is also what an exposed latent bug looks like: identify the earlier defect. Separate an incomplete fix, a latent bug, a pre-existing bug, an intentional change and an unsupported expectation from a confirmed regression, with the evidence for each.
3. **Load.** Read the expected load from `users:` and `growth:` in `## Tabby`, or from the README and deploy config: one person running a script, or many users and processes at once. Judge against that and say which you assumed. Fine for one, wrong for many: check-then-write races, a query per item, a list or cache that only grows, per-process state that must be shared, quadratic work on input a caller controls.
4. **Silenced or weakened checks.** Anything the `tabby` skill forbids silencing, plus its never-miss rules in `development/testing/testing.md`: a new skip or xfail, loosened lint, type or pytest config, a weakened assertion, a deleted test, expected values copied from the code's own output.
5. **Unneeded concepts.** Apply `development/code/minimalism.md` (the deletion test, wrappers, one-implementation abstractions, `utils.py`, unused parameters) to every new function, class, constant and exception, plus an exception that only renames a library error. Check each changed function against the smells files for the area it touches: `development/code/smells.md` always, plus `development/library/smells.md`, `development/testing/smells.md`, `development/application/smells.md` or `development/library/native/smells.md`. A smell is a finding only when you can name the input or situation where it goes wrong.
6. **Docs and comments.** Check against `development/code/comments.md`: conversation residue, restated signatures, negatives that should be behavior. Also a docstring that is wrong for the code.
7. **Public API.** New, renamed or removed names; a changed return type; positional booleans; a missing deprecation warning; a version bump that does not match the change; `__all__` and the changelog not updated.
8. **Dependencies and files.** A second library for a job one already does, a new dependency in the base install, scratch or summary files, unrelated reformatting, hand-edited generated files.
9. **Security.** Anything `development/code/security-basics.md` prohibits, for example `shell=True` with interpolation, f-string SQL, secrets in code or fixtures.

## Slop in a diff

Slop is accidental complexity that came in with the change. Report it as a finding with the line, and only when it is in the diff:

- Comments that narrate or repeat the code; defensive `try`/`except` or `None` checks on data the project's own code produced; casts, `Any` or `# type: ignore` added only to pass the checker; a helper that duplicates one that exists (`git grep`); nesting that early returns would flatten; a wrapper with one caller; leftover prints and scratch files; a style that differs from the file around it.
- Not slop: validation where untrusted data enters, error handling that prevents data loss, security checks, a deprecation shim for a public name, a comment that says why, a test that can fail.

If you wrote the change yourself, none of this is cleaned up afterwards: it is prevented while writing ([minimalism.md](../../tabby/development/code/minimalism.md)). A review of your own work finds what you could not see while writing.

## Closing the review

Give the single most likely thing to break on the most common path, even if it is not the most severe finding. End with what you did not verify: paths you could not reproduce, anything that needs the app or a service running, lines you could not confirm. Never imply you checked more than you opened. Findings that were refuted on a second look ("it is guarded at line N") are worth one line, because they save the next reviewer the same check.

## Deferred shortcuts

List the `# shortcut:` comments the change adds or touches (`git grep -nE "# ?shortcut:"` on the changed files). Each must name its limit and the trigger to revisit it; one that names neither is a finding. A shortcut that names both is a decision, not a finding, unless the expected load already crosses its limit.

## What not to report

- Anything the linter or type checker already enforces and CI already runs.
- Style preferences, naming taste, and "consider" suggestions with no concrete failure.
- Added abstraction, defensive code or tests for cases that cannot happen. If a suggestion is of that kind, drop it.
- Pre-existing problems outside the diff. Mention at most one line, labelled out of scope.
- Complexity ranks (`xenon`, `radon`): a hint, not a finding. Raise it only when you can say what is hard to follow and propose a clearer shape; never ask for a rewrite just to reach an A.
- Speculation about money, units, locales or scale that nothing in the change or the project's use supports.

## Output

Number the findings, ordered by severity, so the author can answer "fix 2 and 5". For each: `file:line`, what is wrong, the input or situation where it fails, and the smallest fix. Then one line: `Checked, no findings: <areas>`. End with a verdict: `request changes` or `no findings`.

A diff with no findings: the verdict plus the `Checked` line, nothing more (at most 10 lines). Format the final report as the `report` default asks (`terse`, `normal`, `audit`; see `development/workflow/shipping.md`).

Where the guidance says to decline findings, say once why you declined, so the author does not wonder whether it was missed.
