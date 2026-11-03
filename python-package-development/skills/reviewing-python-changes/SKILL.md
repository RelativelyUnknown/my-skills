---
name: reviewing-python-changes
description: "Reviews a Python diff for bugs, unneeded abstractions, silenced checks, weakened tests, conversation residue in docs and comments, public API breaks and new dependencies. Use when asked to review a diff, branch or pull request, or before reporting your own work as done."
argument-hint: "[python=3.12 report=normal]"
---

# Reviewing Python changes

Find what is wrong with the diff, and say nothing else. A clean diff gets a short "no findings", not a list of maybes. Prefer a fresh session that did not write the code; a person still reviews multi-file changes.

## Start

1. Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`python.target`, `runner`, `types`, `lint`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts.
2. Read the whole diff (`git diff <base>...<head>`), then the full changed files and the callers of any changed signature.
3. Run `bash <this skill's folder>/scripts/check_new_suppressions.sh <base>...<head>`. It lists added skips, xfails, `type: ignore`, `noqa` and blind `except`; each hit needs a stated reason or is a finding.
4. Run the project's check command only in a way that writes nothing into the work tree (for example `pytest -p no:cacheprovider`) and does not modify files. Do not modify the code under review.

## What to look for, in this order

1. **Correctness.** A variable unassigned on a path (a `try` that can fail before the assignment), swallowed errors, wrong boundary, a mutable default, a result that differs from the docstring. Reproduce it when you can and quote the failing input.
2. **Silenced or weakened checks.** `type: ignore`, `noqa`, `cast`, `Any`, blind `except`, a new skip or xfail, loosened lint, type or pytest config, an assertion reduced to `is not None`, a deleted test, expected values copied from the code's own output.
3. **Unneeded concepts.** Apply the deletion test to every new function, class, constant and exception: if inlining leaves every call site as short and clear, it should not exist. Also: a wrapper around one call, a factory or registry with one implementation, a `utils.py`, a parameter nobody passes, an exception that renames a library error.
4. **Docs and comments.** Conversation residue ("as discussed", "now uses", "previously", "per requirements"), a docstring that is wrong for the code, restated signatures, negatives that should be behavior.
5. **Public API.** New, renamed or removed names; a changed return type; positional booleans; a missing deprecation warning; a version bump that does not match the change; `__all__` and the changelog not updated.
6. **Dependencies and files.** A second library for a job one already does, a new dependency in the base install, scratch or summary files, unrelated reformatting, hand-edited generated files.
7. **Security.** `shell=True` with interpolation, SQL built with f-strings, secrets in code or fixtures, `eval`, `pickle`, `yaml.load`.

## What not to report

- Anything the linter or type checker already enforces and CI already runs.
- Style preferences, naming taste, and "consider" suggestions with no concrete failure.
- Added abstraction, defensive code or tests for cases that cannot happen. If a suggestion is of that kind, drop it.
- Pre-existing problems outside the diff. Mention at most one line, labelled out of scope.
- Complexity ranks (`xenon`, `radon`): a hint, not a finding. Raise it only when you can say what is hard to follow and propose a clearer shape; never ask for a rewrite just to reach an A.
- Speculation about money, units, locales or scale that nothing in the change or the project's use supports.

## Output

For each finding, ordered by severity: `file:line`, what is wrong, the input or situation where it fails, and the smallest fix. Then one line: `Checked, no findings: <areas>`. End with a verdict: `request changes` or `no findings`.

A diff with no findings: the verdict plus the `Checked` line, nothing more (at most 10 lines). Format the final report as the `report=` value asks (`terse`, `normal`, `audit`; see `writing-python-code`).

Where the guidance says to decline findings, say once why you declined, so the author does not wonder whether it was missed.
