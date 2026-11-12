# Security audit: process

Find vulnerabilities an outside party can reach, and report only what you can show. Adapted from the approach of the Cloudflare security-audit skill (MIT, Cloudflare, Inc.), rewritten for Python.

1. **Map the boundaries.** List the entry points (routes, CLI arguments, queue messages, files and environment the process reads) and which side of each is untrusted. A finding needs a named lower-trust party, the input it controls, the control that should stop it, and what crosses the boundary. If one is missing, it is not a finding.
2. **Trace each input to its sinks.** Follow every untrusted value from entry, through parsing, validation and copies, to where it is used: SQL, file paths, URLs, shell and `subprocess`, templates, `eval`, `pickle`/`yaml.load`, `open`, redirects. Include sibling, batch, retry and error paths. Compare what one function guarantees (a length cap, a coercion, an allowlist) with what the next assumes.
3. **Try to disprove each candidate.** Read the controls on the path (allowlists, parameter binding, constant arguments). A value checked against a fixed set, a constant argument list, or a hash used as a cache key is not a vulnerability. A missing best practice with no reachable victim is a hardening note.
4. **Walk the class checklist** ([checklist.md](checklist.md)) for the classes the boundaries make relevant, and record each as clean, not applicable, finding or unverified.
5. **Look for variants.** After a confirmed finding, search for its siblings: the same sink, the same helper, the same missing check on the other routes, jobs and commands. After a fix, try the inputs that would get around it (another encoding, another path to the same sink) and look for what the patch did not cover.
6. **Report** as in [reporting.md](reporting.md).

Judging a candidate:

- **Attacker-controlled or not.** Request data, uploaded files and content, headers, cookies, queue messages from other parties and data written by lower-trust users are attacker-controlled. Settings, environment variables, config files, constants and your own code's output are server-controlled and are not an SSRF, path or command source on their own.
- **Follow the whole enforcement chain.** A check in any layer (middleware, dependency, decorator, the query itself) counts as a control; confirm it holds on every path that reaches the sink before you rate the finding.
- **Do not flag:** tests and fixtures, dead or commented-out code, framework auto-escaping and parameterised ORM queries (flag only their escape hatches used on user data), MD5 for checksums or cache keys, `random` for non-security use, and a path that needs authentication unless the caller is the low-trust party. A diff review reports only what the diff adds; the rest of the code is context.
- **Confidence.** Confirmed (attacker-controlled input reaches the sink) is reported with a severity. Input source unclear goes under `needs validation`. Theoretical or best-practice only is a hardening note at most.

- Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit.
- Facts outside the repository (proxy, identity provider, deployment) are not proof either way: a finding that depends on one is `needs validation` with the question and who can answer it.
- Library and framework defaults depend on the pinned version. Check the version before relying on a default.
- Dependencies, CI workflows and the release path: [supply-chain.md](supply-chain.md).
- Per-class checks and their Python fixes: [security-basics.md](../../tabby/development/code/security-basics.md).
