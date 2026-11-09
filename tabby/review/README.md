# review

Part of the [skills repository](../../README.md). Reviews a Python diff, branch or pull request, audits a project's security, or checks your own change before you report it done. A clean diff or a clean audit gets a short "no findings".

`index.md` points to `references/changes/self-review.md` for reviews and to `references/security-audit/` (`process.md`, `reporting.md`) for audits. The review reads the rule leaves in `python-engineering/references/`, so install both skills. The audit approach (name the boundary, trace input to sink, try to disprove, confirmed / needs-validation / rejected, severity only for confirmed, a fix with a regression test) is adapted in spirit from the Cloudflare security-audit skill (MIT, Cloudflare, Inc.) and written for Python; see [`../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

## Evals

- `evals/clean-diff-no-noise`: a clean diff gets no invented findings.
- `evals/seeded-audit`: a small service with three real vulnerabilities (SQL injection, path traversal, SSRF) and three look-alikes (an allowlisted `ORDER BY`, an allowlisted template name, a constant `subprocess` list with an md5 cache key). Three runs per arm: 1.00 with the skill (fired and read both audit leaves every time), 0.84 without. The bare model already finds the real bugs and rejects the look-alikes; what the leaves add is the report structure (confirmed against needs-validation, a regression test per fix). That gain is on checks derived from the same convention, so it shows the leaves are followed, not that audits get better.

Not built, for lack of a failing baseline: compliance (licences, SBOM, personal data), per-project-type checklists, a cyber-security field of per-class leaves.

MIT.
