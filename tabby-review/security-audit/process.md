# Security audit: process

Find vulnerabilities an outside party can reach, and report only what you can show. Built from Cloudflare's security-audit skill, Sentry's `security-review`, `find-bugs` and `django-access-review`, Anthropic's `claude-code-security-review` and Trail of Bits' review skills (see `THIRD_PARTY_NOTICES.md`), with each technique kept only where it held up when run or traced.

## 1. Scope

- **A diff or pull request:** report only what the change adds or makes reachable; the rest is context you read. **A repository:** start from the entry points. Read the whole diff first, and whole files when the diff is cut off.
- Rank changed files by what they touch, not by size: authentication, authorization, crypto, parsing of outside data, anything that builds a command, query or path, money, and any *removed* check are high; business logic and new public routes medium; tests, docs and logging low. For a high-risk change look at `git log -p` and `git blame` on the lines it removes (why was that check there?), count the callers of a changed function with `git grep`, and see whether a test would fail if the changed lines broke.

## 2. Learn the project's own security model

Before judging a line, find how this project already does the thing: its sanitiser or validator, its authorization decorator, base class, middleware or queryset scoping, its secrets loader, its safe-fetch helper. New code that skips what its siblings do is the best lead; code that uses the project's helper is usually fine. A framework default depends on the pinned version, so read the version.

## 3. Boundaries and flows

1. **Boundaries.** List the entry points (routes, CLI arguments, queue messages, files and environment the process reads) and which side of each is untrusted. A finding names a lower-trust party, the input it controls, the control that should stop it, and what crosses.
2. **Flows.** Follow each untrusted value from entry, through parsing, validation and copies, to where it is used: SQL, file paths, URLs, shell, templates, `eval`, deserializers, redirects. Include sibling, batch, retry and error paths. Compare what one function guarantees (a length cap, a coercion, an allowlist) with what the next assumes.
3. **Classes.** Walk the three class pages for the classes those boundaries make relevant: [injection-and-output.md](injection-and-output.md), [identity-and-access.md](identity-and-access.md), [files-network-and-config.md](files-network-and-config.md). Record each as clean, not applicable, finding or unverified.

Attacker-controlled: request data, uploads and their contents, headers, cookies, messages from other parties, data written by lower-trust users. Server-controlled: settings, environment variables, CLI flags, config files, constants and the project's own output.

## 4. Try to disprove each candidate

The default for every candidate is "refuted" until the evidence says otherwise; reviewers lean toward seeing bugs and overrating them.

- **Restate the claim** in one sentence: the input, the line, the mistake, the effect. If you cannot, drop it. For each finding you keep, you can state the entry point, the payload, how it executes and what the attacker gets.
- **Read the controls on the path:** allowlists, parameter binding, constant arguments, framework escaping, a check in any layer (middleware, dependency, decorator, the query). A check anywhere on the path counts, if it holds on every path that reaches the sink.
- **Ask what the attacker already has.** A bug that needs the privilege it would grant is not a finding. A path behind a login matters only if the caller is the low-trust party and can get the login.
- **Do not report:**
  - tests, fixtures, docs, dead or commented-out code;
  - framework auto-escaping and parameterised queries (only their escape hatches on user data);
  - denial of service, ReDoS, resource exhaustion and missing rate limits (a hardening note, unless a small unauthenticated input causes large amplification);
  - missing audit logs, log forging, missing security headers, open redirects outside login flows, and other hardening-only items;
  - SSRF where the caller controls only the path of a fixed host, and client-side code lacking authorization checks (the server decides);
  - memory-safety claims in code that is not C, C++ or `unsafe`; races and timing attacks that are theoretical;
  - environment variables and CLI flags as attacker input, UUIDs as guessable, and logging of non-secret data;
  - shell scripts and notebooks, unless a concrete path for untrusted input exists;
  - vulnerable versions of third-party libraries in a diff review (a repository audit covers them: [supply-chain.md](supply-chain.md)).
- **Confidence:** reached by attacker-controlled input with no effective control: confirmed, with a severity. Depends on something you cannot see: `needs validation`, with the question. Anything else is a hardening note at most.

## 5. Look for variants, then check the fix

- After a confirmed finding, search for its siblings. Write a pattern that matches only the known instance and make sure it hits; generalise one element at a time (the function, the argument, the module, the framework), reading all matches after each change; stop when more than half are noise. Search beyond the module where you found it: other routes, jobs and commands that reach the same sink, and the same mistake in another form.
- After a fix, try what would get around it (another encoding, another path to the same sink, the same input through the batch endpoint) and read what the patch did not touch.
- A suggested fix must enforce in code. A comment saying the caller must check is not a fix.
- A confirmed finding comes with a regression test that fails before the fix ([reporting.md](reporting.md)).

## Limits

- Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit.
- Facts outside the repository (proxy, identity provider, deployment) are not proof either way: a finding that depends on one is `needs validation`, with the question and who can answer it.
- Dependencies, CI workflows, AI agents in workflows and the release path: [supply-chain.md](supply-chain.md).
- Write-time rules and fixes: `tabby/development/code/security-basics.md`.
