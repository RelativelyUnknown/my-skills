# Security audit: process

Find vulnerabilities an outside party can reach, and report only what you can show. Adapted from the approach of the Cloudflare security-audit skill (MIT, Cloudflare, Inc.), rewritten for Python.

1. **Map the boundaries.** List the entry points (routes, CLI arguments, queue messages, files and environment the process reads) and which side of each is untrusted. A finding needs a named lower-trust party, the input it controls, the control that should stop it, and what crosses the boundary. If one is missing, it is not a finding.
2. **Trace each input to its sinks.** Follow every untrusted value from entry, through parsing, validation and copies, to where it is used: SQL, file paths, URLs, shell and `subprocess`, templates, `eval`, `pickle`/`yaml.load`, `open`, redirects. Include sibling, batch, retry and error paths. Compare what one function guarantees (a length cap, a coercion, an allowlist) with what the next assumes.
3. **Try to disprove each candidate.** Read the controls on the path (allowlists, parameter binding, constant arguments). A value checked against a fixed set, a constant argument list, or a hash used as a cache key is not a vulnerability. A missing best practice with no reachable victim is a hardening note.
4. **Report** as in [reporting.md](reporting.md).

- Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit.
- Facts outside the repository (proxy, identity provider, deployment) are not proof either way: a finding that depends on one is `needs validation` with the question and who can answer it.
- Library and framework defaults depend on the pinned version. Check the version before relying on a default.
- Per-class checks and their Python fixes: [security-basics.md](../../../python-engineering/references/fields/software-engineering/all/code/security-basics.md).
