# review

A module of [Tabby](../SKILL.md) for reviewing a Python diff, branch or pull request, auditing a project's security, and checking your own change before you report it done. A clean diff or a clean audit gets a short "no findings".

**Entry point:** [`index.md`](index.md), about 110 tokens.

## Layout

```
index.md
references/
  changes/self-review.md              silenced checks, weakened tests, needless abstractions, API breaks, new dependencies
  security-audit/process.md           name the boundary, trace input to sink, try to disprove each candidate
  security-audit/reporting.md         confirmed / needs-validation / rejected; severity only for confirmed; a fix with a regression test
  native-boundary.md                  per-function table and checklist for the Python to Rust or C boundary
```

The self-review checks against the rule files in [`../engineering/`](../engineering/), so the two modules ship together. The audit approach is adapted in spirit from the Cloudflare security-audit skill (MIT, Cloudflare, Inc.) and written for Python; see [`../../THIRD_PARTY_NOTICES.md`](../../THIRD_PARTY_NOTICES.md).

## Evals

In [`../evals/`](../evals/):

- `clean-diff-no-noise`: a clean diff gets no invented findings.
- `seeded-audit`: a small service with three real vulnerabilities (SQL injection, path traversal, SSRF) and three look-alikes (an allowlisted `ORDER BY`, an allowlisted template name, a constant `subprocess` list with an md5 cache key).

## Licence

MIT.
