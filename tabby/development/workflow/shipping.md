# Shipping and reporting

Done means the real problem is solved, verified by running the code, and explainable. Passing tests are evidence, not the goal. Before you report done: run the full suite and the project's check command, read your own diff against [smells.md](../code/smells.md), and list every new dependency and every changed or removed test.

## Report (`report`, default `normal`)

Plain and factual. No "production-ready", "robust" or "comprehensive", no celebration, no emojis. Show the exact command and its real output; separate what you verified from what should work.

- `terse`: Verdict, commands run with pass/fail counts, deviations. At most 10 lines. A new dependency, a changed or removed test, or a stopped task always counts as a deviation.
- `normal`: What changed and why, a closing `Noticed:` line (at most three observations from the code you read, or `nothing`), commands with real output, verified vs unverified, every new dependency, every test changed or removed with the reason.
- `audit`: `normal`, plus every shortcut, assumption, skipped check and known limitation (or "none"), everything noticed and left alone, and any rule conflict and which rule won.

## When short is wrong

Short means no filler, never a missing fact. Write full sentences for: a security warning, an action that cannot be undone (confirm before doing it), steps whose order matters, a question you ask the user, and anything a reader repeats back as not understood. Quote an error by its one decisive line, exactly. Text that outlives the conversation (comments, commits, docs, issues) follows the `documentation` module, not the reply style.
