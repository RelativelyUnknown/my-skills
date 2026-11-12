# review

A skill of the Tabby plugin for reviewing a Python diff, branch or pull request, auditing a project's security, and checking your own change before you report it done. A clean diff or a clean audit gets a short "no findings".

**Entry point:** [`SKILL.md`](SKILL.md), about 130 tokens.

## Layout

```
SKILL.md
changes/self-review.md                silenced checks, weakened tests, smells, API breaks, new dependencies
security-audit/process.md             name the boundary, trace input to sink, try to disprove each candidate
security-audit/reporting.md           confirmed / needs-validation / rejected; severity only for confirmed; a fix with a regression test
repo-audit.md                        whole-repository audit: bugs, risk, load, missing tests, what to delete
security-audit/supply-chain.md        package sources, measuring dependency risk, triaging advisories, the release path
security-audit/ci-workflows.md        workflows as authorization code: pwn requests, injection, credentials, runners
security-audit/ci-agents.md           AI agents in workflows: what reaches the prompt, what the agent can do
native-boundary.md                    per-function table and checklist for the Python to Rust or C boundary
design.md                             diagram, animation or interface: a judgment pass and a measured pass, kept apart
```

The self-review checks a change against the rule and smells files in [`../tabby/development/`](../tabby/development/), so the two modules ship together. The audit approach is adapted in spirit from the Cloudflare security-audit skill (MIT, Cloudflare, Inc.) and written for Python; see `THIRD_PARTY_NOTICES.md` at the repository root.

## Evals

In [`../evals/`](../evals/):

- `clean-diff-no-noise`: a clean diff gets no invented findings.
- `seeded-audit`: a small service with three real vulnerabilities (SQL injection, path traversal, SSRF) and three look-alikes (an allowlisted `ORDER BY`, an allowlisted template name, a constant `subprocess` list with an md5 cache key).

## Licence

MIT.
