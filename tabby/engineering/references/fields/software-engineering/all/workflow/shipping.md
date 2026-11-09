# Shipping and reporting

Done means the real problem is solved, verified by running the code, and explainable. Passing tests are evidence, not the goal. Before you report done: run the full suite and the project's check command, read your own diff against [snags.md](../code/snags.md), and list every new dependency and every changed or removed test.

## Report (`report`, default `normal`)

Plain and factual. No "production-ready", "robust" or "comprehensive", no celebration, no emojis. Show the exact command and its real output; separate what you verified from what should work.

- `terse`: Verdict, commands run with pass/fail counts, deviations. At most 10 lines. A new dependency, a changed or removed test, or a stopped task always counts as a deviation.
- `normal`: What changed and why, commands with real output, verified vs unverified, every new dependency, every test changed or removed with the reason.
- `audit`: `normal`, plus every shortcut, assumption, skipped check and known limitation (or "none"), everything noticed and left alone, and any rule conflict and which rule won.
