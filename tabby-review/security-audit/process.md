# Security audit: process

Find vulnerabilities an outside party can reach, and report only what you can show. Ideas from Cloudflare's security-audit skill, Trail of Bits' differential-review, variant-analysis, insecure-defaults and fp-check skills, Sentry's security-review and Anthropic's claude-code-security-review, rewritten for Python; see `THIRD_PARTY_NOTICES.md`.

## 1. Scope and risk

- **A diff or pull request:** report only what the change adds or makes reachable; the rest of the code is context you read, not findings. **A repository:** start from the entry points.
- Rank the changed files by what they touch, not by size: authentication, authorization, crypto, parsing of outside data, anything that runs a command or a query, money, and any *removed* check are high; business logic and new public routes are medium; tests, docs and logging are low. A two-line change in a high file outranks a 500-line change in a low one.
- For a high-risk change: `git log -p` and `git blame` on the lines it removes (why was that check there?), the count of callers of a changed function (`git grep`), and whether the changed lines have a test that would fail if they broke. A security check that is deleted or weakened is the first thing to look for.

## 2. Boundaries and flows

1. **Map the boundaries.** List the entry points (routes, CLI arguments, queue messages, files and environment the process reads) and which side of each is untrusted. A finding needs a named lower-trust party, the input it controls, the control that should stop it, and what crosses the boundary. If one is missing, it is not a finding.
2. **Trace each input to its sinks.** Follow every untrusted value from entry, through parsing, validation and copies, to where it is used: SQL, file paths, URLs, shell and `subprocess`, templates, `eval`, `pickle`/`yaml.load`, `open`, redirects. Include sibling, batch, retry and error paths. Compare what one function guarantees (a length cap, a coercion, an allowlist) with what the next assumes.
3. **Walk the class checklist** ([checklist.md](checklist.md)) for the classes those boundaries make relevant, and record each as clean, not applicable, finding or unverified.

Attacker-controlled: request data, uploaded files and their content, headers, cookies, messages from other parties and data written by lower-trust users. Server-controlled: settings, environment variables, config files, constants and the project's own output; these are not an SSRF, path or command source by themselves (they are a finding only if committed secrets or derived from user input).

## 3. Try to disprove each candidate

LLM reviewers lean toward seeing bugs and overrating them, so the default for every candidate is "refuted" until the evidence says otherwise.

- **Restate the claim** in one sentence: the input, the line, the mistake, the effect. If you cannot, drop it; many candidates end here.
- **Read the controls on the path:** allowlists, parameter binding, constant arguments, framework escaping, a check in any layer (middleware, dependency, decorator, the query). Confirm the control holds on every path that reaches the sink. A value checked against a fixed set, or a hash used as a cache key, is not a vulnerability.
- **Ask what the attacker already has.** A bug that needs the privilege it would grant is not a finding. A path that needs authentication matters only if the caller is the low-trust party.
- **Do not flag:** tests and fixtures, dead code, framework auto-escaping and parameterised queries (flag only their escape hatches used on user data), MD5 for checksums, `random` for non-security use, theoretical or best-practice-only items.
- **Confidence:** reached by attacker-controlled input with no effective control: confirmed, with a severity. Depends on something you cannot see: `needs validation`, with the question. Anything else is a hardening note at most.

## 4. Look for variants, then check the fix

- After a confirmed finding, search for its siblings. Write a pattern that matches only the known instance and make sure it hits; generalise one element at a time (the function, the argument, the module, the framework), reading all matches after each change; stop when more than half are noise. Search outside the module where you found it, other routes, jobs and commands that reach the same sink, and the same mistake in another form.
- After a fix, try what would get around it (another encoding, another path to the same sink, the same input through the batch endpoint) and read what the patch did not touch.
- A confirmed finding comes with a regression test that fails before the fix ([reporting.md](reporting.md)).

## Limits

- Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit.
- Facts outside the repository (proxy, identity provider, deployment) are not proof either way: a finding that depends on one is `needs validation` with the question and who can answer it.
- Library and framework defaults depend on the pinned version. Check the version before relying on a default.
- Dependencies, CI workflows, AI agents in workflows and the release path: [supply-chain.md](supply-chain.md).
- Per-class checks and their Python fixes: [security-basics.md](../../tabby/development/code/security-basics.md).
