# Security audit: process

Find vulnerabilities an outside party can reach, and report only what you can show. Built from Cloudflare's security-audit skill, Sentry's `security-review`, `find-bugs` and `django-access-review`, Anthropic's `claude-code-security-review` and Trail of Bits' review skills (see `THIRD_PARTY_NOTICES.md`), with each technique kept only where it held up when run or traced.

## 1. Scope

- **A diff or pull request:** report only what the change adds or makes reachable; the rest is context you read. **A repository:** start from the entry points. Read the whole diff first, and whole files when the diff is cut off.
- Rank changed files by what they touch, not by size: authentication, authorization, crypto, parsing of outside data, anything that builds a command, query or path, money, and any *removed* check are high; business logic and new public routes medium; tests, docs and logging low. For a high-risk change: `git log -S "<removed text>" --oneline` and `git blame` on the lines it removes (why was that check there? A check added by a commit that says "fix", "security" or a CVE number is the worst one to lose, and so is one added a few weeks ago); `git log -S "<added text>" -p` to see whether the change re-adds code that was removed for a security reason; the number of callers of a changed function (`git grep`), as a rough measure of blast radius; and whether any test would fail if the changed lines broke (a new function with no test, or changed validation with unchanged tests, raises the risk). Treat a refactor as high risk until you have shown it is not: refactors break invariants. Scale depth to size: read everything in a small diff, the first-hop callers in a medium one, the critical paths in a large one.

## 2. Learn the project's own security model

Before judging a line, find how this project already does the thing: its sanitiser or validator, its authorization decorator, base class, middleware or queryset scoping, its secrets loader, its safe-fetch helper. New code that skips what its siblings do is the best lead; code that uses the project's helper is usually fine. A framework default depends on the pinned version, so read the version.

## 3. Boundaries and flows

1. **Boundaries.** List the entry points (routes, CLI arguments, queue messages, files and environment the process reads) and which side of each is untrusted. A finding names a lower-trust party, the input it controls, the control that should stop it, and what crosses.
2. **Flows.** Follow each untrusted value from entry, through parsing, validation and copies, to where it is used: SQL, file paths, URLs, shell, templates, `eval`, deserializers, redirects. Include sibling, batch, retry and error paths. Compare what one function guarantees (a length cap, a coercion, an allowlist) with what the next assumes.
3. **Classes.** Walk the class pages for the classes those boundaries make relevant: [injection-and-output.md](injection-and-output.md), [identity-and-access.md](identity-and-access.md), [files-network-and-crypto.md](files-network-and-crypto.md), [defaults-and-config.md](defaults-and-config.md). Record each as clean, not applicable, finding or unverified.

Attacker-controlled: request data, uploads and their contents, headers, cookies, messages from other parties, data written by lower-trust users. Server-controlled: settings, environment variables, CLI flags, config files, constants and the project's own output. For a value read from a database or file, find out who writes it: if only privileged internal code does, the attacker does not control it. Say how much control the attacker has (full, partial within stated limits such as length or encoding, none) and what is in the way (normalisation, truncation, type coercion).

## 4. Try to disprove each candidate

The default for every candidate is "refuted" until the evidence says otherwise; reviewers lean toward seeing bugs and overrating them.

- **Restate the claim** in one sentence: the input, the line, the mistake, the effect. If you cannot, drop it. For each finding you keep, you can state the entry point, the payload, how it executes and what the attacker gets.
- **Read the controls on the path:** allowlists, parameter binding, constant arguments, framework escaping, a check in any layer (middleware, dependency, decorator, the query). A check anywhere on the path counts, if it holds on every path that reaches the sink.
- **Is the sink reachable at all?** Conditions earlier on the path can make a dangerous-looking line impossible to reach (a branch only entered when `len(x) > 12` makes `x[-4]` safe). Do not report validation or bounds-checking code itself, code that runs only at install or setup time, or debug-only paths as if they were production paths. A failing cleanup of something single-use is defence in depth, not a vulnerability, if the primary control holds.
- **Distinguish what stops exploitation from what only slows it.** A safe type system, a parameterised query, an escaping framework stop it; a rate limit or a hard-to-guess ID raises the bar.
- **Check both directions.** Ask whether you are reporting because the pattern looks dangerous, and whether you are dismissing a real hole because the exploit looks complicated. Re-read the code after you conclude: have you relied on a validation you never saw in the source?
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
- **Reachable, controllable, unprotected** are the three questions. Code nothing calls today is not refuted by that: if it is unprotected, report it at lower severity and say what would make it reachable. If a different protection is in place, record it as a rejected candidate with that protection.
- **Confidence:** reached by attacker-controlled input with no effective control: confirmed, with a severity. Depends on something you cannot see: `needs validation`, with the question. Anything else is a hardening note at most.

## 5. Look for variants, then check the fix

- State the root cause in one sentence: "[untrusted data] reaches [dangerous operation] without [required protection]", or for a logic bug the invariant that is violated ("must return False for anonymous callers; returns True when both IDs are None"). Variants cluster because of habits, copy-paste, an API that invites the same misuse at every call site, a framework idiom, or an incomplete earlier fix: that tells you where to look (sibling files, or everywhere).
- Widen the search before running it: other names that play the same role (grep to confirm they exist: `is_active`, `is_admin`, `is_verified`; `user_id`, `owner_id`), other logic slips of the same kind (inverted condition, `return True` on the fall-through path, `or` for `and`), type edge cases (`None == None`, empty against `None`, zero against `None`), and functions whose behaviour contradicts their name or docstring.
- After a confirmed finding, search for its siblings. Write a pattern that matches only the known instance and make sure it hits; generalise one element at a time (the function, the argument, the module, the framework), reading all matches after each change; stop when more than half are noise. Search beyond the module where you found it: other routes, jobs and commands that reach the same sink, and the same mistake in another form.
- Checking a security fix needs evidence, not the diff, the author or an upstream patch. A test that states the safe outcome must fail on the old code and pass on the new, and you must read the old-code failure to be sure it is your assertion and not an `ImportError` or a typo (a non-zero exit proves nothing). Also: a benign control that works on both; a variant through a different path, not the same payload with another literal (an alternate entry point, a streaming against a buffered mode, the error, cancellation and cleanup paths, empty and maximum inputs, encode against decode, a different ordering); a check that unchanged behaviour is unchanged; an adjacent check that passes on both. Keep the security assertion to the security property: liveness, exact messages and timing belong in separate tests. If a suite fails on the new code, run it on the old before you blame the change.
- "The original proof no longer works" is not a fix until an independent variant also fails to work. "The full suite passes" is not proof the bug was ever reproduced.
- A suggested fix must enforce in code. A comment saying the caller must check is not a fix.
- A confirmed finding comes with a regression test that fails before the fix ([reporting.md](reporting.md)).

## Limits

- Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit.
- Facts outside the repository (proxy, identity provider, deployment) are not proof either way: a finding that depends on one is `needs validation`, with the question and who can answer it.
- Dependencies, CI workflows, AI agents in workflows, the release path and triaging advisories or scanner alerts: [supply-chain.md](supply-chain.md).
- Write-time rules and fixes: `tabby/development/code/security-basics.md`.
