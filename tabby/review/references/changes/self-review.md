# Self-review and diff review

Paths starting `fields/` are under `engineering/references/`.

Find what is wrong with the diff, and say nothing else. A clean diff gets a short "no findings", not a list of maybes. Prefer a fresh session that did not write the code; a person still reviews multi-file changes.

## Start

1. Read the whole diff (`git diff <base>...<head>`), then the full changed files and the callers of any changed signature.
2. List added suppressions: `git diff <base>...<head> -U0 -- '*.py' | grep -nE '^\+[^+].*(pytest\.mark\.(skip|xfail)|type: ignore|noqa|except Exception|except:)'`. Each hit needs a stated reason or is a finding.
3. Run the project's check command only in a way that writes nothing into the work tree (for example `pytest -p no:cacheprovider`) and does not modify files. Do not modify the code under review.

## What to look for, in this order

1. **Correctness.** A variable unassigned on a path (a `try` that can fail before the assignment), swallowed errors, wrong boundary, a mutable default, a result that differs from the docstring. Reproduce it when you can and quote the failing input.
2. **Silenced or weakened checks.** Anything the `engineering` module forbids silencing (its front door), plus the never-miss rules in `fields/software-engineering/all/testing/testing.md`: a new skip or xfail, loosened lint, type or pytest config, a weakened assertion, a deleted test, expected values copied from the code's own output.
3. **Unneeded concepts.** Apply `fields/software-engineering/all/code/minimalism.md` (the deletion test, wrappers, one-implementation abstractions, `utils.py`, unused parameters) to every new function, class, constant and exception, plus an exception that only renames a library error. Check new code against `fields/software-engineering/all/code/snags.md`.
4. **Docs and comments.** Check against `fields/software-engineering/all/code/comments.md`: conversation residue, restated signatures, negatives that should be behavior. Also a docstring that is wrong for the code.
5. **Public API.** New, renamed or removed names; a changed return type; positional booleans; a missing deprecation warning; a version bump that does not match the change; `__all__` and the changelog not updated.
6. **Dependencies and files.** A second library for a job one already does, a new dependency in the base install, scratch or summary files, unrelated reformatting, hand-edited generated files.
7. **Security.** Anything `fields/software-engineering/all/code/security-basics.md` prohibits, for example `shell=True` with interpolation, f-string SQL, secrets in code or fixtures.

## What not to report

- Anything the linter or type checker already enforces and CI already runs.
- Style preferences, naming taste, and "consider" suggestions with no concrete failure.
- Added abstraction, defensive code or tests for cases that cannot happen. If a suggestion is of that kind, drop it.
- Pre-existing problems outside the diff. Mention at most one line, labelled out of scope.
- Complexity ranks (`xenon`, `radon`): a hint, not a finding. Raise it only when you can say what is hard to follow and propose a clearer shape; never ask for a rewrite just to reach an A.
- Speculation about money, units, locales or scale that nothing in the change or the project's use supports.

## Output

For each finding, ordered by severity: `file:line`, what is wrong, the input or situation where it fails, and the smallest fix. Then one line: `Checked, no findings: <areas>`. End with a verdict: `request changes` or `no findings`.

A diff with no findings: the verdict plus the `Checked` line, nothing more (at most 10 lines). Format the final report as the `report` default asks (`terse`, `normal`, `audit`; see `fields/software-engineering/all/workflow/shipping.md`).

Where the guidance says to decline findings, say once why you declined, so the author does not wonder whether it was missed.
